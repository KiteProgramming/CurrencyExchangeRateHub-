import React, { useState, useEffect } from 'react';

const CurrencyExchange = () => {
    const [exchangeRates, setExchangeRates] = useState([]);
    const [currency, setCurrency] = useState('');
    const [rate, setRate] = useState('');

    useEffect(() => {
        // Fetch exchange rates from the backend API
        fetch('/api/exchange-rates/')
            .then(response => response.json())
            .then(data => setExchangeRates(data));
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        // Save the new exchange rate to the backend API
        fetch('/api/exchange-rates/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ currency, rate }),
        })
            .then(response => response.json())
            .then(data => {
                setExchangeRates([...exchangeRates, data]);
                setCurrency('');
                setRate('');
            });
    };

    return (
        <div>
            <h1>Currency Exchange Rates</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Currency"
                    value={currency}
                    onChange={(e) => setCurrency(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Rate"
                    value={rate}
                    onChange={(e) => setRate(e.target.value)}
                />
                <button type="submit">Add Rate</button>
            </form>
            <ul>
                {exchangeRates.map((rate, index) => (
                    <li key={index}>{rate.currency}: {rate.rate}</li>
                ))}
            </ul>
        </div>
    );
};

export default CurrencyExchange;