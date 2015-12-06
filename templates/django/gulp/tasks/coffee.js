var argv         = require('yargs').argv;
var browserSync  = require('browser-sync');
var config       = require('../config').coffee;
var coffee       = require('gulp-coffee');
var gulpif       = require('gulp-if');
var uglify       = require('gulp-uglify');
var gulp         = require('gulp');
var handleErrors = require('../utils/handleErrors');

var production = !!argv.production;

gulp.task('coffee', function () {
    return gulp.src(config.src)
        .pipe(coffee(config.settings))
        .pipe(gulpif(production, uglify()))  // works for production only
        .on('error', handleErrors)
        .pipe(gulp.dest(config.dest))
        .pipe(browserSync.reload({stream:true}));
});
