from mcp.server.fastmcp import FastMCP

mcp = FastMCP("simple-server")


@mcp.tool()
async def multiply(x:str, y:str)-> str:
 '''
 This tool recieves two numbers, multiply them and give result.
 Args:
   x: First number to multiply
   y: Second number to multiply

 Return:
    Product of both
 '''
 output = int(x)*int(y)
 return str(output)

@mcp.tool()
async def divide(x:str , y:str)->str:
 '''
 This tool recieves two numbers, divide them and give result.
 Args:
   x: First number 
   y: Second number

 Return:
    Divsion of both
 '''
 if y == 0 :
   raise Exception("Infinity occurs")
 else:
  output = int(x)/int(y)
  return str(output)


@mcp.tool()
async def add(x:str , y:str)->str:
 '''
 This tool recieves two numbers, addition them and give result.
 Args:
   x: First number 
   y: Second number

 Return:
   Addition of both
 '''
 output = int(x)*int(y)
 return str(output)


@mcp.tool()
async def subtract(x:str , y:str)->str:
 '''
 This tool recieves two numbers, subtract them and give result.
 Args:
   x: First number 
   y: Second number

 Return:
    Subtraction of both
 '''
 output = int(x)-int(y)
 return str(output)


def main():
   mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
