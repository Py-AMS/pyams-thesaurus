
const { src, dest, task, watch, parallel } = require('gulp');

const sass = require('gulp-sass');
const clean = require('gulp-clean-css');
const rename = require('gulp-rename');

sass.compiler = require('node-sass');


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
