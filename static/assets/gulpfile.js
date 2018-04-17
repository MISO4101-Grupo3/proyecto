var gulp = require('gulp'); //default
var sass = require('gulp-sass');//sass complie
var concat = require('gulp-concat'); //compile js plugins into one file
var concatCss = require('gulp-concat-css');//compile css plugins into one file
var watch = require('gulp-watch'); //sass compile to css
var minifyCSS = require('gulp-minify-css'); //minify compiled css

gulp.task('sass', function () {
    return gulp.src('scss/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(minifyCSS())
        .pipe(gulp.dest('css/'));
});
gulp.task('watch', function () {
    gulp.watch('scss/**/*.scss', ['sass']);
});

gulp.task('concat', function () {
    return gulp.src(
        [

        ])
        .pipe(concat('plugins.js'))
        .pipe(gulp.dest('js/plugins/'));
});

gulp.task('concatCss', function () {
    return gulp.src([

    ])
        .pipe(concatCss("plugins/plugins.css"))
        .pipe(gulp.dest('css/'));
});