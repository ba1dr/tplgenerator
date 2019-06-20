var argv        = require('yargs').argv;
var cached      = require('gulp-cached');
var chalk       = require('chalk');
var config      = require('../config').images;
var gulp        = require('gulp');
var imagemin    = require('gulp-imagemin');

var production = !!argv.production;

gulp.task('imageOptimize', function() {
    return gulp.src(config.src + "/" + config.processImages)
        .pipe(cached(imagemin(config.imageminOptions)))
        .pipe(gulp.dest(config.dest));

    // return gulp.src(config.src)
    //     .pipe(gulp.dest(config.dest));
});
