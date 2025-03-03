import React, { useState } from 'react';
import PropTypes from 'prop-types';

const CurrencyExchange = ({ onRateAdded }) => {
    const [pair, setPair] = useState('');
    const [rate, setRate] = useState('');
    const [error, setError] = useState('');

    const validatePair = async (pair) => {
        const [currency1, currency2] = pair.split('-');
        const response = await fetch('http://localhost:8000/api/currencies/');
        const currencies = await response.json();
        const currencyCodes = currencies.map(currency => currency.code);
        return currencyCodes.includes(currency1) && currencyCodes.includes(currency2);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!/^\d+(\.\d{1,6})?$/.test(rate)) {
            setError('Rate must be a numeric value with up to 6 decimal places.');
            return;
        }

        if (!await validatePair(pair)) {
            setError('One or both currencies in the pair are not registered.');
            return;
        }

        // Save the new exchange rate to the backend API
        fetch('http://localhost:8000/api/add-exchange-rate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ pair, rate }),
        })
            .then(response => response.json())
            .then(() => {
                setPair('');
                setRate('');
                onRateAdded(); // Notify parent component to reload exchange rates
            });
    };

    return (
        <div className="container">
            <h1 className="my-4">Manually Add Rates</h1>
            {error && <div className="alert alert-danger">{error}</div>}
            <form onSubmit={handleSubmit} className="mb-4">
                <div className="form-group">
                    <input
                        type="text"
                        className="form-control"
                        placeholder="Currency Pair (e.g., USD-EUR)"
                        value={pair}
                        onChange={(e) => setPair(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <input
                        type="text"
                        className="form-control"
                        placeholder="Rate"
                        value={rate}
                        onChange={(e) => setRate(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary">Add Rate</button>
            </form>
        </div>
    );
};

CurrencyExchange.propTypes = {
    onRateAdded: PropTypes.func.isRequired,
};

export default CurrencyExchange;