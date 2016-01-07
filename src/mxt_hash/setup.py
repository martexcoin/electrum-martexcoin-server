from distutils.core import setup, Extension

mxt_hash_module = Extension('mxt_hash',
                               sources = ['mxtmodule.c',
                                          'mxt.c',
										  'sha3/blake.c',
										  'sha3/bmw.c',
										  'sha3/groestl.c',
										  'sha3/jh.c',
										  'sha3/keccak.c',
										  'sha3/skein.c',
										  'sha3/cubehash.c',
										  'sha3/echo.c',
										  'sha3/luffa.c',
										  'sha3/simd.c',
                                                                                  'sha3/hamsi.c',
                                                                                  'sha3/hamsi_helper.c',
                                                                                  'sha3/fugue.c',
										  'sha3/shavite.c'],

                               include_dirs=['.', './sha3'])

setup (name = 'mxt_hash',
       version = '1.0',
       description = 'Bindings for proof of work used by mxt',
       ext_modules = [mxt_hash_module])
