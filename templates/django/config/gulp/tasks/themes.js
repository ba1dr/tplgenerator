var config  = require('../config');
var gulp    = require('gulp');
var path = require('path');
var folders = require('gulp-folders');
var rename = require("gulp-rename");

gulp.task('themes', function(cb) {
    folders(config.themes.src, function(folder) {
        return gulp.src(path.join(config.themes.src, folder, 'bootstrap.min.css'))
                .pipe(rename(folder + '.min.css'))
                .pipe(gulp.dest(config.themes.dest));
})
    cb();
});
