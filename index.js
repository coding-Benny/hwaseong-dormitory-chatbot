const express = require('express');
const app = express();
const logger = require('morgan');
const bodyParser = require('body-parser');

const apiRouter = express.Router();

app.use(logger('dev', {}));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));

app.use('/api', apiRouter);

apiRouter.post('/sunday', function(req, res) {
  var userInputDay = req.body.action.detailParams.sys_date.origin;
  var dateInfo = req.body.action.params.sys_date;
  var dateObj = JSON.parse(dateInfo);
  var date = dateObj.date;
  var textValue = `${userInputDay}(${date})`;
  const responseBody = {
    version: "2.0",
    template: {
      outputs: [
        {
          simpleText: {
            text: textValue
          }
        }
      ]
    }
  };

  res.status(200).send(responseBody);
});

app.listen(3000, function() {
  console.log('Example skill server listening on port 3000!');
});
   
