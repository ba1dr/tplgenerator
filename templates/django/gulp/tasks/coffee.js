var browserSync  = require('browser-sync');
var config       = require('../config').coffee;
var coffee       = require('gulp-coffee');
var uglify       = require('gulp-uglify');
var gulp         = require('gulp');
var handleErrors = require('../utils/handleErrors');

gulp.task('coffee', function () {
    return gulp.src(config.src)
        .pipe(coffee(config.settings))
        // .pipe(uglify())  // disable for debug, enable for production
        .on('error', handleErrors)
        .pipe(gulp.dest(config.dest))
        .pipe(browserSync.reload({stream:true}));
});
