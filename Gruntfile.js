module.exports = function (grunt) {

  var appConfig = grunt.file.readJSON('package.json');

  // Load grunt tasks automatically
  // see: https://github.com/sindresorhus/load-grunt-tasks
  require('load-grunt-tasks')(grunt);

  // Time how long tasks take. Can help when optimizing build times
  // see: https://npmjs.org/package/time-grunt
  require('time-grunt')(grunt);

  var pathsConfig = function (appName) {
    this.app = appName || appConfig.name;

    return {
      app: this.app,
      css: this.app + '/static/assets/css',
      sass: this.app + '/static/assets/sass',
      fonts: this.app + '/static/assets/fonts',
      images: this.app + '/static/assets/images',
      js: this.app + '/static/assets/js',
      manageScript: 'manage.py'
    };
  };

  grunt.initConfig({

    paths: pathsConfig(),
    pkg: appConfig,
    port: grunt.option('port') || 8000,

    // see: https://github.com/gruntjs/grunt-contrib-watch
    watch: {
      gruntfile: {
        files: ['Gruntfile.js']
      },
      css: {
        files: ['<%= paths.sass %>/**/*.{scss,sass}'],
        tasks: ['sass']
      },
      // compass: {
      //   files: ['<%= paths.sass %>/**/*.{scss,sass}'],
      //   tasks: ['compass:server']
      // },
      livereload: {
        files: [
          '<%= paths.js %>/**/*.js',
          '<%= paths.sass %>/**/*.{scss,sass}',
          '<%= paths.app %>/**/*.html'
          ],
        options: {
          spawn: false,
          livereload: true,
        },
      },
    },

    // see: https://github.com/gruntjs/grunt-contrib-compass
    compass: {
      options: {
          specify: '<%= paths.sass %>/styles.scss',
          sassDir: '<%= paths.sass %>',
          cssDir: '<%= paths.css %>',
          fontsDir: '<%= paths.fonts %>',
          imagesDir: '<%= paths.images %>',
          relativeAssets: false,
          assetCacheBuster: false,
          raw: 'Sass::Script::Number.precision = 10\n'
      },
      dist: {
        options: {
          environment: 'production'
        }
      },
      server: {
        options: {
          // debugInfo: true
        }
      }
    },

    sass: {                              // Task
      dist: {                            // Target
        options: {                       // Target options
          style: 'compressed'
        },
        files: {                         // Dictionary of files
          '<%= paths.css %>/styles.css': '<%= paths.sass %>/styles.scss'
        }
      }
    },

    // see: https://npmjs.org/package/grunt-bg-shell
    bgShell: {
      _defaults: {
        bg: true
      },
      runDjango: {
        cmd: 'python <%= paths.manageScript %> runserver 0.0.0.0:<%= port %>'
      }
    }
  });

  grunt.registerTask('serve', [
    'bgShell:runDjango',
    'watch'
  ]);

  grunt.registerTask('build', [
    'compass:dist'
  ]);

  grunt.registerTask('default', [
    'build'
  ]);

  grunt.registerTask('compile-css', [
    'sass'
  ]);
};