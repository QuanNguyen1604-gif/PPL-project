grammar Cfg;

program: expression EOF;

expression
    : verbs objects location? time? query?
    | verbs objects location? query time?
    | TITLE_STRING
    ;

time: start_time end_time? (today | date) | today | date | duration;

date: INT '/' INT '/' INT ;

today: 'today';

query: ('sunny' | 'cloudy' | 'rainy' | 'windy' | 'snowy' | 'clear' | 'foggy');

start_time: INT ':' INT;

end_time: INT ':' INT;

duration: INT;

objects: STRING;

verbs: ('set' | 'show' | 'check' | 'tell' | 'start' | 'reset');

location: STRING+;

TITLE_STRING: '"' (~["\r\n])* '"';

STRING: [a-zA-Z]+;

INT: [0-9]+;

WS : [ \t\r\n]+ -> skip;
