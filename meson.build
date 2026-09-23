project('where', 'c',
   version : '2.1.3',
   license: 'MIT',
   meson_version: '>=0.64.0',
   default_options : ['warning_level=1']
   )

add_languages('fortran')
add_languages('cython', native: false)
fs = import('fs')

py = import('python').find_installation(pure: false)

np_dep = dependency('numpy')
incdir_f2py = run_command(py,
  ['-c', 'import numpy.f2py; print(numpy.f2py.get_include())'],
  check: true,
).stdout().strip()
f2py_dep = declare_dependency(include_directories: incdir_f2py)

ext_deps = ['sofa', 'gpt2w']

list_src = files('list_sources.py')


# ---------- iers_2010 ----------
run_command(py, files('download.py'), 'iers_2010', check: true)   # <-- whatever argument your Makefile uses
iers_dir = meson.project_source_root() / 'external' / 'iers' / 'src_2010' # <-- your $(IERSDIR)_2010

dehant_lib = static_library('iers_dehant',
  run_command(py, list_src, iers_dir / 'libiers-dehant',
    check: true).stdout().strip().split('\n'),
  pic: true,
)

hardisp_lib = static_library('iers_hardisp',
  run_command(py, list_src, iers_dir / 'libiers-hardisp',
    check: true).stdout().strip().split('\n'),
  pic: true,
)

iers_wrap = custom_target('iers_2010_wrap',
  input: iers_dir / 'iers_2010.pyf',
  output: ['iers_2010module.c', 'iers_2010-f2pywrappers.f'],   # <-- verify by hand, as before
  command: [py, '-m', 'numpy.f2py', '@INPUT@', '--build-dir', '@OUTDIR@'],
)

py.extension_module('iers_2010',
  [
    run_command(py, list_src, iers_dir, check: true).stdout().strip().split('\n'),
    iers_wrap,
    incdir_f2py / 'fortranobject.c',
  ],
  link_with: [dehant_lib, hardisp_lib],
  dependencies: [np_dep, f2py_dep],
  subdir: 'where/ext',
  install: true,
)

# ---------- hf_eop ----------
run_command(py, files('download.py'), 'hf_eop', check: true)

src_dir = meson.project_source_root()/'external'/'iers'/'hfeop'

f_files = run_command(py, list_src, src_dir, check: true).stdout().strip().split('\n')

wrap = custom_target('hf_eop'+'_wrap',
                      input: src_dir/'hfeop_xyu_mod.pyf',
                      output: ['hf_eop' + 'module.c', 'hf_eop' + '-f2pywrappers.f'],
                      command: [py, '-m', 'numpy.f2py', '@INPUT@', '--build-dir', '@OUTDIR@'],
                      )

foreach name : ext_deps
   #download files
   run_command(py, files('download.py'), name, check: true)

   #set src_dir
   src_dir = meson.project_source_root()/'external'/name/'src'

   #Get f files
   f_files = run_command(py, list_src, src_dir, check: true).stdout().strip().split('\n')

   #f2py wrapper generation
   wrap = custom_target(name+'_wrap',
                                   input: src_dir/name+'.pyf',
                                   output: [name + 'module.c', name + '-f2pywrappers.f'],
                                   command: [py, '-m', 'numpy.f2py', '@INPUT@', '--build-dir', '@OUTDIR@'],
                                   )

   #Compile
   py.extension_module(name,
      [f_files, wrap, incdir_f2py/'fortranobject.c'],
      dependencies: [np_dep, f2py_dep],
      subdir: 'where/ext',
      install: true)
endforeach

# ---------- Cython ----------
cython_dirs = ['where/models/orbit', 'where/integrators']

foreach d : cython_dirs
  pyx_files = run_command(py, list_src, meson.project_source_root() / d,
    '--ext', '.pyx', check: true).stdout().strip().split('\n')

  foreach pyx : pyx_files
    py.extension_module(fs.stem(pyx),     # "kepler.pyx" -> module named "kepler"
      pyx,
      cython_args: ['-3', '-X', 'boundscheck=False', '-X', 'cdivision=True'],
      dependencies: [np_dep],
      subdir: d,                          # installs as where/models/orbit/kepler...so
      install: true,
    )
  endforeach
endforeach

install_subdir('where',  install_dir: py.get_install_dir())
install_subdir('config', install_dir: py.get_install_dir())