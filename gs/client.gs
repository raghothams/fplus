
function forecast_plus(xrange, yrange, forecast_period) {
  console.log(xrange);
  console.log(yrange);
  console.log(forecast_period);


  dfdUrl = 'https://cdn.jsdelivr.net/npm/danfojs@1.1.2/lib/bundle.min.js'
  eval(UrlFetchApp.fetch(dfdUrl).getContentText());

  var df = new dfd.DataFrame(yrange, {columns: ['y']});
  var xSeries = new dfd.Series(xrange);
  df.addColumn('x', xSeries,{inplace:true});
  console.log(df.print());
  console.log(df['x'].values);

  var data = {
    'ds': dfd.toDateTime(df['x'].values)['$dateObjectArray'],
    'y': df['y'].values,
    'periods': forecast_period
  }
  console.log(JSON.stringify(data))
  
  var baseURL = 'https://fplus-app.onrender.com'
  var options = {
    'method': 'POST',
    'contentType': 'application/json',
    'payload': JSON.stringify(data)
  };

  var response = UrlFetchApp.fetch(baseURL + '/forecast', options);
  console.log("req fired")
  resp_data = JSON.parse(response.getContentText());

  console.log(resp_data);


  return resp_data.y;
}
