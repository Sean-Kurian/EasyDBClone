

Release/test-exhaustive.objs/%.o: %.cc Makefile
	@echo "CXX $< (Release) for test-exhaustive"
	@mkdir -p $(dir $@)
	@g++ -std=c++11 -Igoogletest/googletest/include -Igoogletest/googletest/ -O3 -Wall  $< -MMD -MF $(@:.o=.d) -c -o $@

Release/test-exhaustive.objs/%.o: %.cpp Makefile
	@echo "CXX $< (Release) for test-exhaustive"
	@mkdir -p $(dir $@)
	@g++ -std=c++11 -Igoogletest/googletest/include -Igoogletest/googletest/ -O3 -Wall  $< -MMD -MF $(@:.o=.d) -c -o $@

Release/test-exhaustive.objs/%.o: %.c Makefile
	@echo "CC $< (Release) for test-exhaustive"
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


Release/test-exhaustive:  Release/objs/test-exhaustive.o Release/objs/googletest/googletest/src/gtest-all.o Release/objs/googletest/googletest/src/gtest_main.o 
	@echo LINK $@
	@g++  Release/objs/test-exhaustive.o Release/objs/googletest/googletest/src/gtest-all.o Release/objs/googletest/googletest/src/gtest_main.o  -pthread  -ldl -o $@
