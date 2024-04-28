/*
 * api.codeslide.net
 *
 * @license
 * Forked from mydraft.cc by Sebastian Stehle
 * Copyright (c) Do Duc Quan. All rights reserved.
*/

const fs = require('fs-extra');

fs.copy('./utils/compile.py', './dist/utils/compile.py')
  .then(() => console.log('compile.py copied successfully'))
  .catch(err => console.error(err));

fs.copy('./utils/parse.py', './dist/utils/parse.py')
  .then(() => console.log('parse.py copied successfully'))
  .catch(err => console.error(err));