import React from 'react';
import CurrencyExchange from './components/CurrencyExchange';
import ManageCurrencies from './components/ManageCurrencies';
import ManualSync from './components/ManualSync';

function App() {
    return (
        <div className="App">
            <CurrencyExchange />
            <ManageCurrencies />
            <ManualSync />
        </div>
    );
}

export default App;