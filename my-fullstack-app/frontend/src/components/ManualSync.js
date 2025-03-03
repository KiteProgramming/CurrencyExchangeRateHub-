import React, { useState } from 'react';
import PropTypes from 'prop-types';

const ManualSync = ({ onSyncComplete }) => {
    const [apiChoice, setApiChoice] = useState('XE');

    const handleSync = () => {
        fetch(`http://localhost:8000/api/manual-sync/?api_choice=${apiChoice}`, {
            method: 'GET',
        })
        .then(response => {
            if (response.ok) {
                alert('Manual sync triggered successfully.');
                onSyncComplete(); // Reload exchange rates
            } else {
                alert('Failed to trigger manual sync.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while triggering manual sync.');
        });
    };

    return (
        <div className="text-center mt-5">
            <div className="form-group">
                <label htmlFor="apiChoice">Select API:</label>
                <select id="apiChoice" className="form-control" value={apiChoice} onChange={(e) => setApiChoice(e.target.value)}>
                    <option value="XE">XE</option>
                    <option value="ExchangeRate-API">ExchangeRate-API</option>
                </select>
            </div>
            <button onClick={handleSync} className="btn btn-primary btn-lg">Call API for the Synchronization of Rates</button>
        </div>
    );
};

ManualSync.propTypes = {
    onSyncComplete: PropTypes.func.isRequired,
};

export default ManualSync;