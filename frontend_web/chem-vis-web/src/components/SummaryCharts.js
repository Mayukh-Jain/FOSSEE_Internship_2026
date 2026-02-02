import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const SummaryCharts = ({ summary }) => {
    if (!summary) {
        return null;
    }

    const typeDistributionData = {
        labels: Object.keys(summary.type_distribution),
        datasets: [
            {
                data: Object.values(summary.type_distribution),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)',
                ],
            },
        ],
    };

    return (
        <div>
            <h3>Equipment Type Distribution</h3>
            <div style={{ width: '50%', margin: 'auto' }}>
                <Pie data={typeDistributionData} />
            </div>
        </div>
    );
};

export default SummaryCharts;
