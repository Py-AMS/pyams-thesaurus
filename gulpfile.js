
const { src, dest, task, watch, parallel } = require('gulp');

const clean = require('gulp-clean-css');
const rename = require('gulp-rename');
const minify = require('gulp-minify');
const sass = require('gulp-sass')(require('node-sass'));


task('sass_dev', function() {
    return src('src/pyams_thesaurus/zmi/resources/sass/thesaurus.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(dest('src/pyams_thesaurus/zmi/resources/css/'));
});

task('sass_prod', function() {
    return src('src/pyams_thesaurus/zmi/resources/sass/thesaurus.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(clean())
        .pipe(rename('thesaurus.min.css'))
        .pipe(dest('src/pyams_thesaurus/zmi/resources/css/'));
});

task('js', function() {
    return src('src/pyams_thesaurus/zmi/resources/js/thesaurus.js')
        .pipe(minify({
            ext: {
                min: '.min.js'
            }
        }))
        .pipe(dest('src/pyams_thesaurus/zmi/resources/js/'));
})

exports.sass_dev = task('sass_dev');
exports.sass_prod = task('sass_prod');
exports.minify_js = task('js');


exports.default = function() {
    watch('src/pyams_thesaurus/zmi/resources/sass/*.scss',
        parallel('sass_dev', 'sass_prod'));
    watch('src/pyams_thesaurus/zmi/resources/js/thesaurus.js',
        parallel('js'));
};
