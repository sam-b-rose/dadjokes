var gulp = require('gulp');
var less = require('gulp-less');
var header = require('gulp-header');
var cleanCSS = require('gulp-clean-css');
var rename = require("gulp-rename");
var uglify = require('gulp-uglify');
var pkg = require('./package.json');

// Set the banner content
var banner = ['/*!\n',
    ' * Sam Rose - <%= pkg.title %> v<%= pkg.version %> (<%= pkg.homepage %>)\n',
    ' * Copyright 2016-' + (new Date()).getFullYear(), ' <%= pkg.author %>\n',
    ' * Licensed under <%= pkg.license.type %> (<%= pkg.license.url %>)\n',
    ' */\n',
    ''
].join('');

var static = 'website/static/';

// Compile LESS files from /less into /css
gulp.task('less', function() {
    return gulp.src(`${static}less/style.less`)
        .pipe(less())
        .pipe(header(banner, { pkg: pkg }))
        .pipe(gulp.dest(static + 'css'));
});

// Minify compiled CSS
gulp.task('minify-css', ['less'], function() {
    return gulp.src(`${static}css/style.css`)
        .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest(`${static}css`));
});

// Minify JS
gulp.task('minify-js', function() {
    return gulp.src(`${static}js/main.js`)
        .pipe(uglify())
        .pipe(header(banner, { pkg: pkg }))
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest(`${static}js`));
});

// Copy vendor libraries from /node_modules into /vendor
gulp.task('copy', function() {
    gulp.src(['node_modules/bootstrap/dist/**/*', '!**/npm.js', '!**/bootstrap-theme.*', '!**/*.map'])
        .pipe(gulp.dest(`${static}vendor/bootstrap`))

    gulp.src(['node_modules/jquery/dist/jquery.js', 'node_modules/jquery/dist/jquery.min.js'])
        .pipe(gulp.dest(`${static}vendor/jquery`))

    gulp.src([
            'node_modules/font-awesome/**',
            '!node_modules/font-awesome/**/*.map',
            '!node_modules/font-awesome/.npmignore',
            '!node_modules/font-awesome/*.txt',
            '!node_modules/font-awesome/*.md',
            '!node_modules/font-awesome/*.json'
        ])
        .pipe(gulp.dest(`${static}vendor/font-awesome`))
})

// Run everything
gulp.task('default', ['less', 'minify-css', 'copy']);

// Dev task
gulp.task('dev', ['less', 'minify-css', 'minify-js'], function() {
    gulp.watch(`${static}less/*.less`, ['less']);
    gulp.watch(`${static}css/*.css`, ['minify-css']);
    gulp.watch(`${static}js/*.js`, ['minify-js']);
});
