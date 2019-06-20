var config      = require('../config');
var del         = require('del');
var gulp        = require('gulp');
// var outputLogo  = require('../utils/outputLogo');

// outputLogo();

gulp.task('build', function(cb) {
          gulp.series(['coffee', 'browserify', 'sass', 'imageOptimize', 'third_party', 'themes'], function(cb1){
    global.isBuilding = false;

    // Delete lingering compiled coffeescript src
    del([config.src + 'js']);
    cb1();
})(cb)});
