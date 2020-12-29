struct TestClass : public rpc::Service<TestClass> {
  TestClass() {
    Export(&TestClass::Method0);
    Export(&TestClass::Method1);
    Export(&TestClass::Method2);
    Export(&TestClass::Method3);
    Export(&TestClass::Method4);
    Export(&TestClass::Method5);
    Export(&TestClass::Method6);
    Export(&TestClass::Method7);
    Export(&TestClass::Method8);
    Export(&TestClass::Method9);
    Export(&TestClass::Method10);
    Export(&TestClass::Method11);
    Export(&TestClass::Method12);
    Export(&TestClass::Method13);
    Export(&TestClass::Method14);
    Export(&TestClass::Method15);
  }
  long Method0(int, std::string, int, long, std::string, int, long, long, std::string, long, std::string, int, int, int) { return 7252227729850979318L; }
  long Method1(long, std::string, int, std::string, long, long) { return 4868247320682670285L; }
  std::string Method2(int, std::string, long, std::string, int, long, long, std::string, int, int, long, std::string, long, long, std::string, std::string, std::string, int, std::string, long, int, int, long, int, std::string, int, std::string, long, std::string, std::string, long) { return std::string("-E|oqei.9Qw%i+z/ "); }
  int Method3(long, long, int, long) { return 240611083; }
  int Method4(int, std::string, long, long, long, std::string, long, std::string, long, int, long, long, int, std::string, int, std::string, int, int, long, int, long, std::string) { return 2046453948; }
  long Method5(std::string, int, int, int, int, long, long, int, int, int, long, std::string, long, long, long, int, int, int, int, std::string, std::string, int, int, std::string, std::string, std::string, long) { return 7572858286578551992L; }
  int Method6(std::string, long, long, std::string, long, int, long, long, long, long, int, long, int, int, long, int, int, long, long, long, long, std::string, std::string, std::string, long, long, int, int, long, long) { return 2005260651; }
  std::string Method7(std::string) { return std::string("l+==:S4%l$<1Qz|zTEj&$3[.%vQ"); }
  long Method8(std::string, long, std::string, int, std::string, long, int, int, int, int, std::string, long, std::string, int, long, long, int, int) { return 4645416760923683447L; }
  int Method9() { return 223683494; }
  std::string Method10(long, int, long, long, long, int, int, long, std::string, long, int, int, std::string, long, long, std::string, long, int, long, long, long, long) { return std::string("Cy-)J6VK|W2Q 1k%"); }
  long Method11(int, int, int, std::string, std::string, std::string, int, std::string, long, std::string, int, int, long) { return 6813216840997990288L; }
  long Method12(std::string, int, int, std::string, int, std::string, long, std::string, std::string, int, long, std::string, std::string, std::string, std::string, std::string, int, std::string, int, int, std::string, std::string, std::string, long, std::string, std::string, int, std::string) { return 7029297268641121639L; }
  std::string Method13(std::string, std::string, long, int, std::string, int, long, std::string, std::string, std::string, long, long, std::string, std::string, std::string, std::string, std::string, std::string, int, int, std::string, std::string, long, long) { return std::string("vW*9}C73$en=;n"); }
  std::string Method14(int, std::string, long, int, long, std::string, std::string, long, int, std::string, int, int, std::string, long, int, std::string, int, long, long, int, std::string, long, std::string, std::string, int, int, int) { return std::string("pvx)nzJd"); }
  std::string Method15(std::string, int, int, std::string, long, int, std::string, long, std::string, int, int, long, int, int, long, int, std::string, std::string) { return std::string("I0C@)I,sqa:B"); }
};
struct Test : public ServiceTestUtil { void Run() {
SetUpServer(); srv->AddService(new TestClass(), 30082);
SetUpClient(); auto s = new TestClass(); s->set_instance_id(30082);
{  auto r = client->Call(s, &TestClass::Method0, 1329074362, std::string("pK!;45[}N5! '|SP+sm1>"), 348185157, 7788076349227249237L, std::string("rL)%s v?/P7kOf}Mc%H4"), 1509737770, 8099679541654728615L, 2525900052918254000L, std::string("6rY|e$&gw#^5%ke=T2!R"), 7425478094724160572L, std::string("&y%V#C8JV+!SmV"), 773683759, 1010058520, 1046471228);
  client->Flush();
  assert(!r->has_error()); assert(r->data() == 7252227729850979318L);
}
{  auto r = client->Call(s, &TestClass::Method1, 2499034208867031004L, std::string("}ryR&z#c`UiWZ@W{U~Ra"), 1884694170, std::string("L#Z#z26(r1zia}eaaC7HzneOj<"), 1350488606363076886L, 7396173257039416533L);
  client->Flush();
  assert(!r->has_error()); assert(r->data() == 4868247320682670285L);
}
{  auto r = client->Call(s, &TestClass::Method2, 75474016, std::string("NyHF-[N|lGfKEL-%lDMd41"), 4234944593298333819L, std::string("b:B/YfZQ/[jMXUt<!;f"), 135479037, 196421457190446030L, 5156298541948546762L, std::string("axJ^C+ue:PMq~YpZB?0w1LuI3fdP"), 41667427, 1060662075, 4457083942180941468L, std::string("plMgOg5|W1WHhvdxnvBa@Sa(82"), 8764090168862058401L, 2683925312603634735L, std::string("3i!w:h*4=;hf$_K|K?<"), std::string("`ole({:8=7hM~iE6OOJmg1Tkp"), std::string("e==#H}r5`x1w.K/vy"), 433850476, std::string("<A1ii{QzP>kM$&j$New`Cmn;{8Hp"), 6708657282467267774L, 142614996, 348917848, 5971834500275030968L, 962114706, std::string("XgZ)#CT$J<)"), 907307655, std::string("}TCkC_d[("), 378343820628274659L, std::string("7N^I.8.eA1'r3Q0<D07xS :"), std::string("au85^t7r@u<L.K2M6@lgM&*]=#/:="), 2528335948929351383L);
  client->Flush();
  assert(!r->has_error()); assert(r->data() == std::string("-E|oqei.9Qw%i+z/ "));
}
{  auto r = client->Call(s, &TestClass::Method3, 4668316872697272133L, 1184520672054295334L, 792658667, 5897480467134055186L);
  client->Flush();
  assert(!r->has_error()); assert(r->data() == 240611083);
}
{  auto r = client->Call(s, &TestClass::Method4, 1131654894, std::string("{7EGGr]0kC[rM90MEHke"), 9160909744384892781L, 1347160696455060006L, 4350787934785443439L, std::string("FM.?eSd*FcdTO(0BRFP"), 2118289717183628309L, std::string("fO;`jlDPa"), 7613039274618548132L, 898280369, 632278917513731316L, 4047936394207634911L, 89129831, std::string("OM< RLB&so!]hg"), 1498670233, std::string("EtmiELQ@=X~^EfFt4cqg-2j}h[hPe"), 1411188783, 1483959175, 3965163128072359036L, 2023942383, 3826152664017134754L, std::string(";<f:z,}?~0#pt- ,#EdhrKRh&"));
  client->Flush();
  assert(!r->has_error()); assert(r->data() == 2046453948);
}
{  auto r = client->Call(s, &TestClass::Method5, std::string("E!%S<>7S7DNVC^V1Pc2-l2ORzB}J"), 187321103, 1292793346, 2139278828, 1940838265, 8549456553203331707L, 6822035464793678030L, 935378820, 1589688982, 431634285, 4428201253832930403L, std::string("^wy2&Hv8UcG&6?"), 6613161893874741927L, 985848524060030660L, 2565970598525222382L, 1520422461, 440528410, 964898921, 961317722, std::string("X+4^bO:ZG"), std::string("`oDvE%;H9[nG@@WU9g=.0r9D"), 1927662814, 1621126641, std::string("iS972)X&KZAqsy`9"), std::string("}po7U*Fbz%IYv3*0J"), std::string("6#B^^aPOX1hp/W]D*hgmcD"), 163715453497708447L);
  client->Flush();
  assert(!r->has_error()); assert(r->data() == 7572858286578551992L);
}
{  auto r = client->Call(s, &TestClass::Method6, std::string("fA&vh?*i_hEA:tvH[gU0Fy:/a%o#ty~"), 6383397910204921953L, 7363680069667608262L, std::string("DYk!@1BW#:|^Rk"), 8699217071367982516L, 1373495187, 6024251299018689138L, 853074260139603542L, 1914450607902898126L, 4299683828407226739L, 548117090, 6730563716110441845L, 1758785833, 852219496, 3069445671599648758L, 523388088, 909929333, 2870443385649001688L, 2155839504372613820L, 5557754128562929018L, 8370024231733714034L, std::string("!vOKzS$C_#jX2t`"), std::string("D< q6Jaiui8!p7t=bo?6s`vt=^J"), std::string("Q(0uD-dZWFBN0WL!nA<"), 7857649515412284553L, 7168518533418646368L, 1141709619, 185405160, 2764135992188776607L, 4779926935925548811L);
  client->Flush();
  assert(!r->has_error()); assert(r->data() == 2005260651);
}
{  auto r = client->Call(s, &TestClass::Method7, std::string("$fC1Ye>>=ve_Br5"));
  client->Flush();
  assert(!r->has_error()); assert(r->data() == std::string("l+==:S4%l$<1Qz|zTEj&$3[.%vQ"));
}
{  auto r = client->Call(s, &TestClass::Method8, std::string("q$*.S8f64!o&X%>Yib"), 517085231533291862L, std::string("'bbzE@:5U"), 1310833566, std::string("V02'Ey=W"), 7141372971298387503L, 156892368, 1484447248, 1415583141, 806991743, std::string("yXo:}wyao<+RT.Y+<l3acM6^Xp,"), 376156904917286968L, std::string("_C!v?uq!e. m`T|89ow"), 894736954, 3735457277173911482L, 2971616654643908011L, 1223121010, 1973477130);
  client->Flush();
  assert(!r->has_error()); assert(r->data() == 4645416760923683447L);
}
{  auto r = client->Call(s, &TestClass::Method9);
  client->Flush();
  assert(!r->has_error()); assert(r->data() == 223683494);
}
{  auto r = client->Call(s, &TestClass::Method10, 7631259825544829098L, 1989957461, 6455563768858772254L, 3701049337667717887L, 8838689985500479017L, 1273255071, 1176937466, 3848048852472140234L, std::string("#ez }W6 E/b`>$Q;N($*>-eHU5B~GJE"), 6191114665172357918L, 2061379192, 1200046785, std::string("t^):jlw&mIB=QCDl"), 6257732424398880065L, 4115840548401382902L, std::string("U~`|D,*aQ3S-=n"), 4280251226568744280L, 917512825, 5883189741618401083L, 7639861163504383992L, 4851160858820405878L, 4086845896077795911L);
  client->Flush();
  assert(!r->has_error()); assert(r->data() == std::string("Cy-)J6VK|W2Q 1k%"));
}
{  auto r = client->Call(s, &TestClass::Method11, 16969512, 261051180, 792207241, std::string("2q01S*R41.He;bT1i;1^"), std::string("Lk'/<Q>t"), std::string("Qd<_8F3tZD "), 924507130, std::string("8b[JLtX);%tB1.s"), 1841861615231406689L, std::string("{h<[}bko"), 1160761612, 1755746032, 77458388648897798L);
  client->Flush();
  assert(!r->has_error()); assert(r->data() == 6813216840997990288L);
}
{  auto r = client->Call(s, &TestClass::Method12, std::string("%{qLEf%N(@E6O6cP4_6P941"), 301458565, 358976691, std::string("6mdLr]>@$%BO$GpF^"), 827943364, std::string("Bmn !<95M>6vR!Y~s7:18<Qh"), 8474518973078385585L, std::string("dWs?w^+w_G1quO%i&C}vX8&pQWVoP*T"), std::string("zp}Y{u6C'%6S*!S-DQ%yg+h9_?&0JZ6"), 1963835192, 1767576720047398585L, std::string("D'0e+6{_@|0K?aM9FU]5?cE"), std::string("<Y,dj&'r7l}MhZj"), std::string("j3&J`<p6?KK^-qEIHN+3U"), std::string("&i{4eY{IE0LlphZ(('P"), std::string("4?&ZgUe{(uqq!#T[~}!,Jj}1E"), 1266356463, std::string("LSz]s!5[SxT"), 1706924434, 1322455273, std::string("J]XJ31G12SY|Qj@Q!"), std::string("#xHsw]OKV%%BYL!/w4A?B"), std::string("rxKBcksbUs[zgSY5|-7P"), 6361886678903526031L, std::string("|F_>b~lVx5uY!f<S[uOCI)"), std::string("C3oE`]q/[5kvxk`"), 607118634, std::string("uB>v)XHaNw&t}[91I[r$M~_ckT"));
  client->Flush();
  assert(!r->has_error()); assert(r->data() == 7029297268641121639L);
}
{  auto r = client->Call(s, &TestClass::Method13, std::string("W2&9)EW|N-E.[=4Q;ljJ3C:8"), std::string("6tRI)VY/lbTB_ O#.,=?]V*E"), 5533233452655640450L, 368939124, std::string("UWNH'Nn0%H<"), 84052184, 5654727318483833723L, std::string("hkakvm&4H>j"), std::string("[Qu/&BW+pF8roUbw@t],"), std::string("I$BM8k*SSh,[;)}o1k4I_!{"), 6377931126315977827L, 2645623464254501095L, std::string("Il}J/K_wV3I<@KtXQpIbZ"), std::string("<[&TCq)j[%2gPr`$&"), std::string("=CR3|$Ca`}kzY"), std::string("W+3F5}71ig!Gi'N$H~7E!8hbv"), std::string("Oq=?FHRiZNkqUW]z>aIB*"), std::string("ZOFo5*fxVU6uxEb7sK'M^+|yjC<ti"), 300162748, 731700674, std::string("dW7HNm~d`tA'UVw!ZF#6N|09"), std::string("L,(AN8##PKQ;G4|=R!r)xs"), 996229794049341342L, 6536161414294762020L);
  client->Flush();
  assert(!r->has_error()); assert(r->data() == std::string("vW*9}C73$en=;n"));
}
{  auto r = client->Call(s, &TestClass::Method14, 1954215340, std::string("'-T.2rYKu]xA/1f@.$s/sy&d[BY"), 4441453985711988471L, 846424198, 8670996314572930559L, std::string(",9c{p,nN%-Z3s{BtoNhfTNBt%u KM+y"), std::string("B]O3i>^kK6~@2>2~m{c?G&4"), 6259997336460773342L, 1254865753, std::string("C:oyYMIi4dH ._"), 259670716, 189949693, std::string(";]k&YOE!UWKLi"), 491313571399020494L, 1001345126, std::string("j[X1ElskiKeM7!+#$"), 439215086, 4159110167771829859L, 8877325272635752620L, 388659629, std::string("OeJ?fU'?.6bw*N^,vEV.Ca"), 6605024198047172675L, std::string("[o#^n/.TZK8-RX<e"), std::string("1ofpx]3OhV/w{PTkS0W`<)8g?E7w^"), 1195445228, 1695897551, 911672235);
  client->Flush();
  assert(!r->has_error()); assert(r->data() == std::string("pvx)nzJd"));
}
{  auto r = client->Call(s, &TestClass::Method15, std::string("vadQt1:H@0Ena.?qc "), 4006541, 425706378, std::string("r)^(}=&++piR"), 2301098835951378037L, 1294437388, std::string("%{GpZR.L3.X}DH' P&:S.FB1-t^"), 3572694277608858112L, std::string("kYC3G}bRHva}q#"), 1877351373, 39202025, 837755448570350444L, 20458338, 1323309366, 1826777009805269865L, 1204917931, std::string("9kZtR.=>g`N-1_%> v>Cm>"), std::string("fV[n4C%|zzO*8mn"));
  client->Flush();
  assert(!r->has_error()); assert(r->data() == std::string("I0C@)I,sqa:B"));
}
TearDownServer(); TearDownClient();
}};
extern "C" void __invoke() { Test().Run(); }
