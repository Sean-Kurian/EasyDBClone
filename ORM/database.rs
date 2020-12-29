/*
 * database.rs
 *
 * Implementation of EasyDB database internals
 *
 * University of Toronto
 * 2019
 */

use packet::{Command, Request, Response, Value};
use std::collections::HashMap;
use schema::*;
 
/* OP codes for the query command */
pub const OP_AL: i32 = 1;
pub const OP_EQ: i32 = 2;
pub const OP_NE: i32 = 3;
pub const OP_LT: i32 = 4;
pub const OP_GT: i32 = 5;
pub const OP_LE: i32 = 6;
pub const OP_GE: i32 = 7;

/* You can implement your Database structure here
 * Q: How you will store your tables into the database? */
 #[derive(Debug)]
pub struct Row {
    values: Vec<Value>,
    version: i64,
}

#[derive(Debug)]
pub struct Database {
    data_tables: HashMap<i32, HashMap<i64, Row>>, // hm<tbidx, hm<rowidx, values>>
    type_tables: HashMap<i32, Table>,
    next_ids: HashMap<i32, i64>,
}

impl Database {
    pub fn new(table_schema: Vec<Table>) -> Database {
        let mut type_tables = HashMap::new();
        let mut data_tables = HashMap::new();
        let mut next_ids = HashMap::new();
        
        // map type_tables
        for table in table_schema.into_iter() {
            data_tables.insert(table.t_id, HashMap::new());
            next_ids.insert(table.t_id, 1);
            type_tables.insert(table.t_id, table);
        }
            
        Database {
            data_tables: data_tables,
            type_tables: type_tables,
            next_ids: next_ids,
        }
    }
}

/* Receive the request packet from client and send a response back */
pub fn handle_request(request: Request, db: & mut Database) 
    -> Response  
{           
    /* Handle a valid request */
    let result = match request.command {
        Command::Insert(values) => 
            handle_insert(db, request.table_id, values),
        Command::Update(id, version, values) => 
             handle_update(db, request.table_id, id, version, values),
        Command::Drop(id) => handle_drop(db, request.table_id, id),
        Command::Get(id) => handle_get(db, request.table_id, id),
        Command::Query(column_id, operator, value) => 
            handle_query(db, request.table_id, column_id, operator, value),
        /* should never get here */
        Command::Exit => Err(Response::UNIMPLEMENTED),
    };
    
    /* Send back a response */
    match result {
        Ok(response) => response,
        Err(code) => Response::Error(code),
    }
}


/*
 * TODO: Implment these EasyDB functions
 */
fn check_value_type_for_column(col: &Column, value: &Value, db: &Database) 
    -> i32  // code 
{
    match value {
        Value::Null => Response::BAD_VALUE,

        Value::Integer(_) if col.c_type == Value::INTEGER => Response::OK,
        Value::Integer(_) => Response::BAD_VALUE,

        Value::Float(_) if col.c_type == Value::FLOAT => Response::OK,
        Value::Float(_) => Response::BAD_VALUE,

        Value::Text(_) if col.c_type == Value::STRING => Response::OK,
        Value::Text(_) => Response::BAD_VALUE,

        Value::Foreign(row_id) if col.c_type == Value::FOREIGN => {
            // find the table it is referencing
            let foreign_table_id = col.c_ref;
            let foreign_table_resp = db.data_tables.get(&foreign_table_id);
            let foreign_table: &HashMap<i64, Row>;

            if let Some(rows_ref) = foreign_table_resp {
                foreign_table = rows_ref;
            } else {
                return Response::BAD_TABLE;    // foreign table not found
            }

            let row_resp = foreign_table.get(&row_id);
            if let Some(_) = row_resp {
                Response::OK
            } else {
                Response::BAD_FOREIGN
            }
        },
        _ => Response::BAD_VALUE
    }
}

fn handle_insert(db: & mut Database, table_id: i32, values: Vec<Value>) 
    -> Result<Response, i32> 
{
    let db_type_tables = &db.type_tables;   // get all types tables
    let tb_resp = db_type_tables.get(&table_id);    // get types table search response
    let type_tb_ref: &Table;    // will hold the types table

    if let Some(tb_ref) = tb_resp {
        type_tb_ref = tb_ref;
    } else {
        return Err(Response::BAD_TABLE);    // table does not exist
    }
    
    if type_tb_ref.t_cols.len() != values.len() {
        return Err(Response::BAD_ROW);  // BAD_ROW: missing or too many values
    }

    for i in 0..values.len() {  // check values are valid
        let code = check_value_type_for_column(&type_tb_ref.t_cols[i], &values[i], db);
        if code == Response::BAD_VALUE || code == Response::BAD_FOREIGN {
            return Err(code);
        }
    }

    let db_data_tables = &mut db.data_tables;
    let tb_resp = db_data_tables.get_mut(&table_id);
    let data_tb_ref: &mut HashMap<i64, Row>;    // data table to update

    if let Some(tb_ref) = tb_resp { // get the data table
        data_tb_ref = tb_ref;
    } else {
        panic!("type and data tables mismatch: missing data table entry");
    }

    let next_ids_resp = db.next_ids.get_mut(&table_id);
    let new_row_id: &mut i64;
    if let Some(id) = next_ids_resp {   // get the next unique id to use (no recycling)
        new_row_id = id;
    } else {
        panic!("type and next_id mismatch: missing next_id entry");
    }

    data_tb_ref.insert(*new_row_id, Row {
        values: values,
        version: 1, // will always begin with version 1
    });

    *new_row_id += 1;   // update the next unique id for this table
    
    return Ok(Response::Insert(*new_row_id - 1, 1));
}

fn handle_update(db: & mut Database, table_id: i32, object_id: i64, 
    version: i64, values: Vec<Value>) -> Result<Response, i32> 
{
    let db_type_tables = &db.type_tables;   // get all types tables
    let tb_resp = db_type_tables.get(&table_id);    // get types table search response
    let type_tb_ref: &Table;    // will hold the types table

    if let Some(tb_ref) = tb_resp {
        type_tb_ref = tb_ref;
    } else {
        return Err(Response::BAD_TABLE);    // table does not exist
    }
    
    if type_tb_ref.t_cols.len() != values.len() {
        return Err(Response::BAD_ROW);  // BAD_ROW: missing or too many values
    }

    for i in 0..values.len() {  // check values are valid
        let code = check_value_type_for_column(&type_tb_ref.t_cols[i], &values[i], db);
        if code == Response::BAD_VALUE || code == Response::BAD_FOREIGN {
            return Err(code);
        }
    }

    let db_data_tables = &mut db.data_tables;
    let tb_resp = db_data_tables.get_mut(&table_id);
    let data_tb_ref: &mut HashMap<i64, Row>;    // data table to update

    if let Some(tb_ref) = tb_resp { // get the data table
        data_tb_ref = tb_ref;
    } else {
        panic!("type and data tables mismatch: missing data table entry");
    }

    let obj_resp = data_tb_ref.get_mut(&object_id);
    let obj_ref: &mut Row;
    if let Some(r_ref) = obj_resp {
        obj_ref = r_ref;
    } else {
        return Err(Response::NOT_FOUND);
    }

    if version != 0 && version != obj_ref.version {
        return Err(Response::TXN_ABORT);
    }

    obj_ref.values = values;
    obj_ref.version += 1;

    return Ok(Response::Update(obj_ref.version));
}

fn handle_drop(db: & mut Database, table_id: i32, object_id: i64) 
    -> Result<Response, i32>
{
    //let db_data_tables = &mut db.data_tables; 
    let db_type_tables = &mut db.type_tables; 
    let tb_resp = db_type_tables.get_mut(&table_id); 



    if let Some(tb_ref) = tb_resp {

    } else {
        return Err(Response::BAD_TABLE);    // table does not exist
    }

  
    let mut foreign_table_ids = vec![];

    for (key, val) in db_type_tables{ //Iterate through all tables
        for (idx, i) in val.t_cols.iter().enumerate(){ //Iterate through all columns in a table with the index = idx
            if i.c_ref == table_id{ //If this is the foreign_table we're looking for
                foreign_table_ids.push((*key, idx)); 
            }
        }
    }


    let mut things_to_drop = vec![];
    
    for (key, idx) in foreign_table_ids{ //Iterate through stored key/index pairs of foreign tables
        if let Some(db_data_tables_row) = db.data_tables.get_mut(&key){ //db_data_tables_row is a HashMap containing row_id and row
            for (key2, val2) in db_data_tables_row{
                match val2.values[idx]{ //Check row.values at foreign table index, is always foreign
                    Value::Foreign(row_id) => if row_id == object_id {
                        things_to_drop.push((key, *key2)); //To avoid second mutable borrow, store in list and call in loop after
                    },
                    _ => panic!("error, everything should be foreign"),
                }
            }
        }
    }

    for (i, j) in things_to_drop{ //Drop all things in list
        handle_drop(db, i, j);
    }

    
    if let Some(db_data_tables_row) = db.data_tables.get_mut(&table_id){
        db_data_tables_row.remove(&object_id); 
    }
    else{
        return Err(Response::BAD_TABLE); 
    }
    return Ok(Response::Drop); 
}

fn handle_get(db: & Database, table_id: i32, object_id: i64) 
    -> Result<Response, i32>
{
    let db_data_tables = &db.data_tables;
    let tb_resp = db_data_tables.get(&table_id);
    let data_tb_ref: &HashMap<i64, Row>;

    if let Some(tb_ref) = tb_resp {
        data_tb_ref = tb_ref;
    } else {
        return Err(Response::BAD_TABLE);
    }

    let row_resp = data_tb_ref.get(&object_id);
    let row_ref: &Row;

    if let Some(r_ref) = row_resp {
        row_ref = r_ref;
    } else {
        return Err(Response::NOT_FOUND);
    }

    return Ok(Response::Get(row_ref.version, &row_ref.values));
}

fn handle_query(db: & Database, table_id: i32, column_id: i32,
    operator: i32, other: Value) 
    -> Result<Response, i32>
{

    let db_type_tables = &db.type_tables;   // get all types tables
    let tb_resp = db_type_tables.get(&table_id);    // get types table search response
    let type_tb_ref: &Table;    // will hold the types table

    if let Some(tb_ref) = tb_resp {
        type_tb_ref = tb_ref;
    } else {
        return Err(Response::BAD_TABLE);    // table does not exist
    }


    //Column ID in range
    if column_id == 0 && operator == OP_AL{

    }
    else if column_id < 1 || column_id > type_tb_ref.t_cols[type_tb_ref.t_cols.len()-1].c_id{
        return Err(Response::BAD_QUERY);
    }
    else if type_tb_ref.t_cols[(column_id as usize)-1].c_type == Value::FOREIGN{  //Only OP_NE and OP_EQ can work w Foreign
        if operator != OP_NE && operator != OP_EQ{
            return Err(Response::BAD_QUERY); 
        }
    }
    else if operator == OP_AL && column_id != 0{
        return Err(Response::BAD_QUERY); 
    }

    match other{
        Value::Integer(_) => if type_tb_ref.t_cols[(column_id as usize)-1].c_type != 1{
            return Err(Response::BAD_QUERY); 
        }, 
        Value::Float(_) => if type_tb_ref.t_cols[(column_id as usize)-1].c_type != 2{
            return Err(Response::BAD_QUERY); 
        }, 
        Value::Text(_) => if type_tb_ref.t_cols[(column_id as usize)-1].c_type != 3{
            return Err(Response::BAD_QUERY); 
        }, 
        Value::Foreign(_) => if type_tb_ref.t_cols[(column_id as usize)-1].c_type != 4{
            return Err(Response::BAD_QUERY); 
        },
        Value::Null => (),  
    }





    let mut row_ids = vec![];
    match operator{
        OP_AL => //println!("cool!"), 
        for (key, val) in &db.data_tables[&table_id]{
            println!("HIE"); 
            row_ids.push(*key); 
            println!("row ids: {:?}", row_ids); 
        }, 
        
        OP_EQ => 
        for (key, val) in &db.data_tables[&table_id]{ 
            if val.values[column_id as usize - 1] == other{
                //println!("val: {:?} other: {:?}", val.values[column_id as usize - 1], other);
                row_ids.push(*key); 
            }
        }, 
        OP_NE => 
        for (key, val) in &db.data_tables[&table_id]{ 
            if val.values[column_id as usize - 1] != other{
                //println!("val: {:?} other: {:?}", val.values[column_id as usize - 1], other);
                row_ids.push(*key); 
            }
        },
        OP_LT => 
        for (key, val) in &db.data_tables[&table_id]{ 
            if val.values[column_id as usize - 1] < other{
                //println!("val: {:?} other: {:?}", val.values[column_id as usize - 1], other);
                row_ids.push(*key); 
            }
        },
        OP_GT => 
        for (key, val) in &db.data_tables[&table_id]{ 
            if val.values[column_id as usize - 1] > other{
                //println!("val: {:?} other: {:?}", val.values[column_id as usize - 1], other);
                row_ids.push(*key); 
            }
        }, 
        OP_LE =>
        for (key, val) in &db.data_tables[&table_id]{ 
            if val.values[column_id as usize - 1] <= other{
                //println!("val: {:?} other: {:?}", val.values[column_id as usize - 1], other);
                row_ids.push(*key); 
            }
        }, 
        OP_GE => 
        for (key, val) in &db.data_tables[&table_id]{ 
            if val.values[column_id as usize - 1] >= other{
                //println!("val: {:?} other: {:?}", val.values[column_id as usize - 1], other);
                row_ids.push(*key); 
            }
        }, 
        _ => return Err(Response::BAD_QUERY), 
    }

    //println!("{:?}", row_ids); 
    return Ok(Response::Query(row_ids)); 
}

