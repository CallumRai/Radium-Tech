# Radium

## Structure
    .
    ├── examples                   # Contains specific tests/case studies
    ├── helpers
    |   ├──  data.py               # Functions to call signal data
    |   ├──  plots.py              # Functions to plot data
    |   ├──  test.py               # Functions to test data
    
## To be done

* Globalise key so it doesn't have to be included as a parameter of every function 
* Cleverly parameterise functions to reduce amount required e.g. daily_two_close() -> plot_signals(daily, two, close)
