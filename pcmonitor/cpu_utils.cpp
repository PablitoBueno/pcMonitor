#include "cpu_utils.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <vector>
#include <utility>
#include <string>

// Função para definir o governador da CPU
void set_governor(int core_id, const char* governor) {
    std::ostringstream command;
    command << "cpupower -c " << core_id << " frequency-set -g " << governor;
    if (system(command.str().c_str()) != 0) {
        throw std::runtime_error("Erro ao configurar o governador!");
    }
}

// Função para ajustar a frequência de um núcleo
void adjust_freq(int core_id, int min_freq, int max_freq) {
    std::ostringstream command;
    command << "cpupower -c " << core_id 
            << " frequency-set -d " << min_freq << "MHz -u " << max_freq << "MHz";
    if (system(command.str().c_str()) != 0) {
        throw std::runtime_error("Erro ao ajustar a frequência!");
    }
}

// Função para obter temperaturas dos núcleos
std::vector<std::pair<std::string, float>> get_temperatures() {
    std::vector<std::pair<std::string, float>> temperatures;

    std::ifstream file("/sys/class/thermal/thermal_zone0/temp");
    if (!file.is_open()) {
        throw std::runtime_error("Não foi possível abrir o arquivo de temperatura.");
    }

    std::string line;
    while (std::getline(file, line)) {
        float temp = std::stof(line) / 1000.0;  // Conversão para Celsius
        temperatures.push_back({"core", temp});
    }

    return temperatures;
}
