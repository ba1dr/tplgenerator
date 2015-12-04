var config  = require('../config').third_party;
var gulp    = require('gulp');
var uglify  = require('gulp-uglify');
var concat  = require('gulp-concat');

gulp.task('third_party', function () {
    gulp.src(config.css)
        .pipe(concat('dependencies.min.css'))
        .pipe(gulp.dest(config.dest.css));

    gulp.src(config.js)
        .pipe(concat('dependencies.js'))
        // .pipe(uglify())  // disable for debug, enable for production
        .pipe(gulp.dest(config.dest.js));

    gulp.src(config.fonts)
        .pipe(gulp.dest(config.dest.fonts));
});
