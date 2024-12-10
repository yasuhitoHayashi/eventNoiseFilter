from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import pybind11

# 拡張モジュールの定義
ext_modules = [
    Extension(
        'filter_events',  # モジュール名
        ['filter_events.cpp'],  # コンパイルする C++ ファイル
        include_dirs=[pybind11.get_include()],  # pybind11 のヘッダファイルディレクトリ
        language='c++',  # 使用する言語
        extra_compile_args=['-O3', '-std=c++11'],  # 最適化と C++11 標準を有効化
    ),
]

# setup 関数
setup(
    name='filter_events',  # パッケージ名
    version='0.1',
    author='Your Name',
    description='A Python module for event filtering implemented in C++ with pybind11',
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},  # setuptools の build_ext を指定
    zip_safe=False,  # zip_safe を False に設定
)

#python3 setup.py build_ext --inplace