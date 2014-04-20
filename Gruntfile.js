module.exports = function(grunt) {

  // Project Configuration
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    jasmine: {
      deku: {
        src: [
          'js/models/*.js',
          'js/collections/*.js',
          'js/views/*.js',
          'js/app.js'
        ],
        options: {
          vendor: [
            'js/lib/jquery.min.js',
            'bower_components/jasmine-jquery/lib/jasmine-jquery.js',
            'js/lib/bootstrap.min.js',
            'js/lib/jquery.flippy.min.js',
            'js/lib/masonry.pkgd.min.js',
            'js/lib/slidebars.min.js',
            'js/lib/underscore-min.js',
            'js/lib/backbone-min.js'
            'js/lib/backbone-min.js',
            'js/lib/bootbox.min.js',
            'js/lib/tag-it.min.js',
            'js/lib/bootstrap-tagsinput.min.js'
          ],
          specs: 'spec/*Spec.js',
          helpers: 'spec/*Helper.js'
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-jasmine');
}
