Traceback (most recent call last):
  File "/Users/tungnguyen/Project/TravelKB/.venv/bin/markitdown", line 10, in <module>
    sys.exit(main())
             ^^^^^^
  File "/Users/tungnguyen/Project/TravelKB/.venv/lib/python3.12/site-packages/markitdown/__main__.py", line 196, in main
    result = markitdown.convert(
             ^^^^^^^^^^^^^^^^^^^
  File "/Users/tungnguyen/Project/TravelKB/.venv/lib/python3.12/site-packages/markitdown/_markitdown.py", line 283, in convert
    return self.convert_local(source, stream_info=stream_info, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/tungnguyen/Project/TravelKB/.venv/lib/python3.12/site-packages/markitdown/_markitdown.py", line 333, in convert_local
    with open(path, "rb") as fh:
         ^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'raw/assets/ĐXĐ THAILAND 5N4D.xlsx'
