from conans import ConanFile, CMake

class LibActiveObjectConan(ConanFile):
  settings = "os", "compiler", "build_type", "arch"
  generators = "cmake"
  default_options = "gtest:shared=False" #, "OpenSSL:shared=True"


  def config(self):
    if self.scope.dev and self.scope.build_tests:
      self.requires( "gtest/1.8.0@lasote/stable" )

  def imports(self):
    self.copy("*.dll", dst="bin", src="bin") # From bin to bin
    self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin

  def build(self):
    cmake = CMake(self.settings)
    flag_build_tests = "-DBUILD_UNIT_TESTS=1" if self.scope.dev and self.scope.build_tests else ""
    self.run('cmake "%s" %s %s' % (self.conanfile_directory, cmake.command_line, flag_build_tests))
    self.run('cmake --build . %s' % cmake.build_config)
    if self.scope.dev and self.scope.build_tests:
      self.run('make unit_test')
