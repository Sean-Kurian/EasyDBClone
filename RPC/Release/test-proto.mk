

Release/test-proto.objs/%.o: %.cc Makefile
	@echo "CXX $< (Release) for test-proto"
	@mkdir -p $(dir $@)
	@g++ -std=c++11 -Igoogletest/googletest/include -Igoogletest/googletest/ -O3 -Wall  $< -MMD -MF $(@:.o=.d) -c -o $@

Release/test-proto.objs/%.o: %.cpp Makefile
	@echo "CXX $< (Release) for test-proto"
	@mkdir -p $(dir $@)
	@g++ -std=c++11 -Igoogletest/googletest/include -Igoogletest/googletest/ -O3 -Wall  $< -MMD -MF $(@:.o=.d) -c -o $@

Release/test-proto.objs/%.o: %.c Makefile
	@echo "CC $< (Release) for test-proto"
	@mkdir -p $(dir $@)
	@cc    $< -MMD -MF $(@:.o=.d) -c -o $@

Release/objs/%.o: %.cc Makefile
	@echo "CXX $< (Release)"
	@mkdir -p $(dir $@)
	@g++ -std=c++11 -Igoogletest/googletest/include -Igoogletest/googletest/ -O3 -Wall $< -MMD -MF $(@:.o=.d) -c -o $@

Release/objs/%.o: %.cpp Makefile
	@echo "CXX $< (Release)"
	@mkdir -p $(dir $@)
	@g++ -std=c++11 -Igoogletest/googletest/include -Igoogletest/googletest/ -O3 -Wall $< -MMD -MF $(@:.o=.d) -c -o $@

Release/objs/%.o: %.c Makefile
	@echo "CC $< (Release)"
	@mkdir -p $(dir $@)
	@cc   $< -MMD -MF $(@:.o=.d) -c -o $@


Release/test-proto:  Release/objs/rpc.o Release/objs/test-proto.o Release/objs/googletest/googletest/src/gtest-all.o Release/objs/googletest/googletest/src/gtest_main.o 
	@echo LINK $@
	@g++  Release/objs/rpc.o Release/objs/test-proto.o Release/objs/googletest/googletest/src/gtest-all.o Release/objs/googletest/googletest/src/gtest_main.o  -pthread   -o $@
