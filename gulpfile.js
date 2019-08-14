// Initialize modules
// Importing specific gulp API functions lets us write them below as series() instead of gulp.series()
const {src, dest, watch, series, parallel} = require('gulp');
// Importing all the Gulp-related packages we want to use
const sourcemaps = require('gulp-sourcemaps');
const sass = require('gulp-sass');
const concat = require('gulp-concat');
const uglify = require('gulp-uglify');
const postcss = require('gulp-postcss');
const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');
const replace = require('replace-in-file');
const browserSync = require('browser-sync').create()
const exec = require('child_process').exec;


// File paths
const files = {
    sassPath: 'src/sass/**/*.sass',
    jsPath: 'src/js/**/*.js'
};

// Sass task: compiles the style.sass file into style.css
function sassTask() {
    return src(files.sassPath)
        .pipe(sourcemaps.init()) // initialize sourcemaps first
        .pipe(sass()) // compile sass to CSS
        .pipe(concat('main.css'))
        .pipe(postcss([autoprefixer(), cssnano()])) // PostCSS plugins
        .pipe(sourcemaps.write('.')) // write sourcemaps file in current directory
        .pipe(dest('bhtml/static/dist')
        ); // put final CSS in dist folder
}

// JS task: concatenates and uglifies JS files to script.js
function jsTask() {
    return src([files.jsPath])
        .pipe(sourcemaps.init()) // initialize sourcemaps first
        .pipe(concat('main.js'))
        .pipe(uglify())
        .pipe(sourcemaps.write('.')) // write sourcemaps file in current directory
        .pipe(dest('bhtml/static/dist')
        );
}

// Cachebust
function cacheBustTask() {
    var cbString = new Date().getTime();
    console.log('New cache bust string: ' + cbString);
    replace.sync({
        files: 'bhtml/templates/base.html',
        from: /cb=\d+/g,
        to: 'cb=' + cbString,
    });
    return Promise.resolve('cache busted')
}

// Watch task: watch sass and JS files for changes
// If any change, run sass and js tasks simultaneously
function watchTask() {
    watch([files.sassPath, files.jsPath],
        series(
            parallel(
                sassTask,
                jsTask,
                cacheBustTask
            ),
            browserSyncReload
        )
    )
}

function browserSyncTask() {
    browserSync.init({
        notify: false,
        port: 8080,
        proxy: 'localhost:8000'
    });
}

function browserSyncReload() {
    browserSync.reload();
    return Promise.resolve('browserSync reloaded')
}

// Export the default Gulp task so it can be run
// Runs the sass and js tasks simultaneously
// then runs cacheBust, then watch task
exports.default = series(
    parallel(
        sassTask,
        jsTask
    ),
    cacheBustTask,
    watchTask
);

exports.build = series(
    parallel(
        sassTask,
        jsTask
    ),
    cacheBustTask
);

exports.buildJS = series(
    jsTask
);

exports.buildCSS = series(
    sassTask
);

exports.cacheBust = series(
    cacheBustTask
);

exports.browserSync = parallel(
    watchTask,
    browserSyncTask
);
