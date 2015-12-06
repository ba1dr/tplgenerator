var argv    = require('yargs').argv;
var config  = require('../config').third_party;
var gulp    = require('gulp');
var gulpif       = require('gulp-if');
var uglify  = require('gulp-uglify');
var concat  = require('gulp-concat');

var production = !!argv.production;

gulp.task('third_party', function () {
    gulp.src(config.css)
        .pipe(concat('dependencies.min.css'))
        .pipe(gulp.dest(config.dest.css));

    gulp.src(config.js)
        .pipe(concat('dependencies.js'))
        .pipe(gulpif(production, uglify()))  // works for production only
        .pipe(gulp.dest(config.dest.js));

    gulp.src(config.fonts)
        .pipe(gulp.dest(config.dest.fonts));

    gulp.src(config.statics)
        .pipe(gulp.dest(config.dest.statics));
});
