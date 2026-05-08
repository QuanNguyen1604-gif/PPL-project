# PPL Assistant Refined

Đây là phiên bản được dựng lại **dựa trên project zip gốc** của bạn. Ý tưởng cốt lõi vẫn giữ nguyên:
- dùng **CFG + ANTLR** để parse câu lệnh tiếng Anh đơn giản,
- trích xuất ý định bằng visitor,
- điều hướng sang các module `calendar`, `weather`, `pomodoro`,
- hỗ trợ cả **CLI chat** và **Tkinter GUI**.

## Điểm mình đã làm lại
- bổ sung **parser/lexer đã generate sẵn** để project chạy được ngay,
- sửa cấu trúc thành package Python rõ ràng,
- sửa đường dẫn file bằng `pathlib` để chạy ổn định từ mọi thư mục,
- thống nhất tên file Pomodoro cho hệ điều hành phân biệt hoa thường,
- tách `response_engine`, `parser_service`, `modules`,
- thêm **interactive CLI** và **test tự động**,
- giữ nguyên data mẫu nhưng làm project sạch hơn để nộp môn PPL.

## Kiến trúc
- `Cfg.g4`: grammar của ngôn ngữ lệnh
- `assistant/parser_service.py`: lexer/parser service
- `assistant/extractor_visitor.py`: trích xuất command fields
- `assistant/response_engine.py`: điều phối command
- `assistant/modules/calendar.py`: lịch / meeting / event
- `assistant/modules/weather.py`: thời tiết
- `assistant/modules/pomodoro.py`: pomodoro timer state
- `assistant/ui.py`: giao diện Tkinter
- `main.py`: entry point

## Cách chạy
### 1. Cài package
```bash
pip install -r requirements.txt
```

### 2. Chạy CLI chat
```bash
python main.py --chat
```

### 3. Chạy một lệnh đơn
```bash
python main.py --command "show weather vung tau 16/12/2024"
```

### 4. Chạy GUI
```bash
python main.py --gui
```

## Ví dụ lệnh
```text
show calendar 30/12/2024
show meeting 30/12/2024
show event 31/12/2024
show weather vung tau 16/12/2024
tell weather quang ngai sunny 17/12/2024
set pomodoro 25
start pomodoro
reset pomodoro
set event 13:30 04/01/2025
"My project presentation"
```

## Luồng PPL để thuyết trình
1. **Lexical + syntax analysis**: ANTLR đọc grammar `Cfg.g4` và sinh lexer/parser.
2. **Parse tree**: đầu vào được parse theo CFG.
3. **Visitor-based semantic extraction**: visitor chuyển parse tree thành `Command`.
4. **Semantic dispatch**: engine chuyển `Command` sang module nghiệp vụ phù hợp.
5. **Stateful dialogue**: thao tác `set event/...` có trạng thái chờ tiêu đề.

## Chạy test
```bash
python -m pytest -q
```
### Bonus: Chạy KEY API cho weather
```bash
$env:OPENWEATHER_API_KEY = "PASTE YOUR API KEY";