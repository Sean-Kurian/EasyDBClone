

Release/test-complex.objs/%.o: %.cc Makefile
	@echo "CXX $< (Release) for test-complex"
	@mkdir -p $(dir $@)
	@g++ -std=c++11 -Igoogletest/googletest/include -Igoogletest/googletest/ -O3 -Wall  $< -MMD -MF $(@:.o=.d) -c -o $@

Release/test-complex.objs/%.o: %.cpp Makefile
	@echo "CXX $< (Release) for test-complex"
	@mkdir -p $(dir $@)
	@g++ -std=c++11 -Igoogletest/googletest/include -Igoogletest/googletest/ -O3 -Wall  $< -MMD -MF $(@:.o=.d) -c -o $@

Release/test-complex.objs/%.o: %.c Makefile
	@echo "CC $< (Release) for test-complex"
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


Release/test-complex:  Release/objs/rpc.o Release/objs/test-complex.o Release/objs/googletest/googletest/src/gtest-all.o Release/objs/googletest/googletest/src/gtest_main.o 
	@echo LINK $@
	@g++  Release/objs/rpc.o Release/objs/test-complex.o Release/objs/googletest/googletest/src/gtest-all.o Release/objs/googletest/googletest/src/gtest_main.o  -pthread   -o $@
