const fs = require('fs-extra');

fs.copy('./utils/compile.py', './dist/utils/compile.py')
  .then(() => console.log('compile.py copied successfully'))
  .catch(err => console.error(err));

fs.copy('./utils/parse.py', './dist/utils/parse.py')
  .then(() => console.log('parse.py copied successfully'))
  .catch(err => console.error(err));