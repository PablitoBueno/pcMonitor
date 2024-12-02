from setuptools import setup, Extension
from Cython.Build import cythonize

# Define a extensão Cython + C++ com as configurações corretas
ext_modules = [
    Extension(
        name="coreAdjust",
        sources=["coreAdjust.pyx", "cpu_utils.cpp"],  # Inclua o arquivo C++ aqui
        language="c++",  # Especifica que a linguagem é C++
        extra_compile_args=["-std=c++11"],  # Usando a versão moderna do C++
        include_dirs=["/home/Pablito/Documentos/pcmonitor/"],  # Diretório atual para cabeçalhos
    )
]

# Chama o setuptools para compilar a extensão
setup(
    ext_modules=cythonize(ext_modules)
)
