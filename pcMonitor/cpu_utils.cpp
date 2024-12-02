#include "cpu_utils.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <vector>
#include <utility>
#include <string>

// Function to set the CPU governor
void set_governor(int core_id, const char* governor) {
    std::ostringstream command;
    command << "cpupower -c " << core_id << " frequency-set -g " << governor;
    if (system(command.str().c_str()) != 0) {
        throw std::runtime_error("Error setting governor!");
    }
}

// Function to adjust the frequency of a core
void adjust_freq(int core_id, int min_freq, int max_freq) {
    std::ostringstream command;
    command << "cpupower -c " << core_id 
            << " frequency-set -d " << min_freq << "MHz -u " << max_freq << "MHz";
    if (system(command.str().c_str()) != 0) {
        throw std::runtime_error("Error adjusting frequency!");
    }
}
