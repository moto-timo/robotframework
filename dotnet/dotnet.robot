*** Settings ***
Library	C:/Projects/robotframework/StaticExampleLibrary/bin/Debug/StaticExampleLibrary.dll

*** Test Cases ***
Simple .NET Test
	Simple Keyword
	Greet	Robot Framework
	Greet	World

Returning Value
	${result}=	Multiply By Two	4.1
	Numbers Should Be Equal	${result}	8.2

Failing Test
	Numbers Should Be Equal	2	2
	Numbers Should Be Equal	2	3