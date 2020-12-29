/*
 * server.rs
 *
 * Implementation of EasyDB database server
 *
 * University of Toronto
 * 2019
 */

use std::net::TcpListener;
use std::net::TcpStream;
use std::io::Write;
use std::io;
use std::sync::Arc;
use std::sync::Mutex;
use std::thread;
use packet::Command;
use packet::Response;
use packet::Network;
use schema::Table;
use database;
use database::Database;

/*
fn single_threaded(listener: TcpListener, table_schema: Vec<Table>, verbose: bool)
{
    /* 
     * you probably need to use table_schema somewhere here or in
     * Database::new 
     */
    let mut db = Database::new(table_schema);

    for stream in listener.incoming() {
        let stream = stream.unwrap();
        
        if verbose {
            println!("Connected to {}", stream.peer_addr().unwrap());
        }
        
        match handle_connection(stream, &mut db) {
            Ok(()) => {
                if verbose {
                    println!("Disconnected.");
                }
            },
            Err(e) => eprintln!("Connection error: {:?}", e),
        };
    }
}
*/

fn multi_threaded(listener: TcpListener, table_schema: Vec<Table>, verbose: bool)
{
    let db = Database::new(table_schema);
    let mut threads = vec![];

    let db_mutex = Arc::new(Mutex::new(db));
    let count_mutex = Arc::new(Mutex::new(0));

    for stream in listener.incoming() {
        let stream = stream.unwrap();
        let db_ref = Arc::clone(&db_mutex);
        let count_ref = Arc::clone(&count_mutex);
        
        if verbose {
            println!("Connected to {}", stream.peer_addr().unwrap());
        }
        
        threads.push(
            thread::spawn(move || {
                match handle_connection(stream, &db_ref, &count_ref) {
                    Ok(()) => {
                        if verbose {
                            println!("Disconnected.");
                        }
                    },
                    Err(e) => eprintln!("Connection error: {:?}", e),
                };
            })
        );
    }
    
    for t in threads.into_iter() {  // wait for threads to finish
        t.join().unwrap();
    }
}

/* Sets up the TCP connection between the database client and server */
pub fn run_server(table_schema: Vec<Table>, ip_address: String, verbose: bool)
{
    let listener = match TcpListener::bind(ip_address) {
        Ok(listener) => listener,
        Err(e) => {
            eprintln!("Could not start server: {}", e);
            return;
        },
    };
    
    println!("Listening: {:?}", listener);
    
    /*
     * TODO: replace with multi_threaded
     */
    multi_threaded(listener, table_schema, verbose);
}

impl Network for TcpStream {}

/* Receive the request packet from ORM and send a response back */
fn handle_connection(mut stream: TcpStream, db_ref: & Arc<Mutex<Database>>, count_ref: & Arc<Mutex<i32>>) 
    -> io::Result<()> 
{
    /* 
     * Tells the client that the connction to server is successful.
     * TODO: respond with SERVER_BUSY when attempting to accept more than
     *       4 simultaneous clients.
     */
    
    let mut count = count_ref.lock().unwrap();
    if *count == 4 {
        stream.respond(&Response::Error(Response::SERVER_BUSY))?;
        return Ok(());
    }
    *count += 1;
    std::mem::drop(count);  // unlock so other threads can access if need

    stream.respond(&Response::Connected)?;

    loop {
        let request = match stream.receive() {
            Ok(request) => request,
            Err(e) => {
                /* respond error */
                stream.respond(&Response::Error(Response::BAD_REQUEST))?;
                let mut count = count_ref.lock().unwrap();  // decrease count
                *count -= 1;
                return Err(e);
            },
        };
        
        /* we disconnect with client upon receiving Exit */
        if let Command::Exit = request.command {
            break;
        }
        
        /* Send back a response */
        let mut db = db_ref.lock().unwrap();
        let response = database::handle_request(request, &mut *db);
        
        stream.respond(&response)?;
        stream.flush()?;
    }

    let mut count = count_ref.lock().unwrap();  // decrease count
    *count -= 1;

    Ok(())
}

