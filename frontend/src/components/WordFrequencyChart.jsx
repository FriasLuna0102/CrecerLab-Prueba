import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function WordFrequencyChart({ frequentWords = [], chartType = 'bar', onChartTypeChange }) {
  const { t } = useTranslation();
  const [chartData, setChartData] = useState([]);
  const [setColorMap] = useState({});

  useEffect(() => {
    if (!frequentWords || !frequentWords.length) {
      setChartData([]);
      return;
    }

    const newColorMap = {};
    const colors = [
      '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
      '#ec4899', '#6366f1', '#14b8a6', '#f97316', '#a855f7'
    ];

    const sortedWords = [...frequentWords].sort((a, b) => b.count - a.count);

    const formattedData = sortedWords.map((item, index) => {
      newColorMap[item.word] = colors[index % colors.length];

      return {
        name: item.word,
        count: item.count,
        fill: colors[index % colors.length]
      };
    });

    setChartData(formattedData);
  }, [frequentWords]);

  const handleChartTypeChange = (e) => {
    if (onChartTypeChange) {
      onChartTypeChange(e.target.value);
    }
  };

  const renderChart = () => {
    if (chartData.length === 0) {
      return (
        <div className="no-data-message">
          {t('articleDetail.noDataAvailable')}
        </div>
      );
    }

    if (chartType === 'horizontal') {
      return (
        <ResponsiveContainer width="100%" height={400}>
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{ top: 20, right: 30, left: 80, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis
              dataKey="name"
              type="category"
              width={80}
              tick={{ fontSize: 12 }}
            />
            <Tooltip
              formatter={(value) => [`${value} ${t('articleDetail.occurrences')}`, t('articleDetail.frequency')]}
              labelFormatter={(value) => `"${value}"`}
            />
            <Legend />
            <Bar
              dataKey="count"
              name={t('articleDetail.wordFrequency')}
              fill="#3b82f6"
            />
          </BarChart>
        </ResponsiveContainer>
      );
    }

    return (
      <ResponsiveContainer width="100%" height={400}>
        <BarChart
          data={chartData}
          margin={{ top: 20, right: 30, left: 20, bottom: 80 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="name"
            angle={-45}
            textAnchor="end"
            height={80}
            tick={{ fontSize: 12 }}
          />
          <YAxis />
          <Tooltip
            formatter={(value) => [`${value} ${t('articleDetail.occurrences')}`, t('articleDetail.frequency')]}
            labelFormatter={(value) => `"${value}"`}
          />
          <Legend />
          <Bar
            dataKey="count"
            name={t('articleDetail.wordFrequency')}
            fill="#3b82f6"
          />
        </BarChart>
      </ResponsiveContainer>
    );
  };

  return (
    <div className="word-frequency-chart">
      <div className="chart-header">
        <h3>{t('articleDetail.wordFrequencyVisualization')}</h3>
        <div className="chart-controls">
          <label htmlFor="chart-type">{t('articleDetail.chartType')}:</label>
          <select
            id="chart-type"
            value={chartType}
            onChange={handleChartTypeChange}
            className="chart-type-selector"
          >
            <option value="bar">{t('articleDetail.verticalBar')}</option>
            <option value="horizontal">{t('articleDetail.horizontalBar')}</option>
          </select>
        </div>
      </div>
      <div className="chart-container">
        {renderChart()}
      </div>
    </div>
  );
}

export default WordFrequencyChart;
