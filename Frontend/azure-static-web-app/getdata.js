var http = require('http');
var fs = require('fs');

function send404error(response)
{
	response.writeHead(404, {"Content-Type":"text/plain"});
	response.write("404 Error!");
	response.end();
}

function sendcheck(response)
{
	response.writeHead(200, {"Content=Type":"text/plain"});
	response.write("제출되었습니다!");
	response.end();

}

function onAir(request, response)
{
	if(request.method == 'GET' && request.url == "/")
	{
		response.writeHead(200,{"Content-Type": "text/html"});
		fs.createReadStream("./add.html").pipe(response);

	}
	else
	{
		send404error(response);
	}
}


http.createServer(onAir).listen(8080);
console.log("Server Started");

getdata().listen(8080);
