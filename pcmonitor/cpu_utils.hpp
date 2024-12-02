#ifndef CPU_UTILS_HPP
#define CPU_UTILS_HPP

#include <string>
#include <vector>

extern "C" {
    void set_governor(int core_id, const char* governor);
    void adjust_freq(int core_id, int min_freq, int max_freq);
    std::vector<std::pair<std::string, float>> get_temperatures();
}

#endif
