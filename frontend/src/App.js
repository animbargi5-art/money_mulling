import React, { useState, useEffect } from 'react';
import { Layout, Card, Form, Input, Button, Table, Tag, notification, Statistic, Row, Col, Tabs, Alert, Space } from 'antd';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import axios from 'axios';
import './App.css';

const { Header, Content } = Layout;
const { TabPane } = Tabs;

function App() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({ total: 0, high: 0, medium: 0, low: 0 });
  const [networkStatus, setNetworkStatus] = useState(null);
  const [testAccount, setTestAccount] = useState(null);

  const [form] = Form.useForm();

  useEffect(() => {
    fetchNetworkStatus();
  }, []);

  const fetchNetworkStatus = async () => {
    try {
      const response = await axios.get('/api/network-status');
      setNetworkStatus(response.data);
    } catch (error) {
      console.error('Failed to fetch network status:', error);
    }
  };

  const createTestAccount = async () => {
    try {
      const response = await axios.post('/api/create-account');
      if (response.data.success) {
        setTestAccount(response.data.account);
        notification.success({
          message: 'Test Account Created',
          description: 'New Algorand testnet account created successfully!'
        });
      }
    } catch (error) {
      notification.error({
        message: 'Account Creation Failed',
        description: error.response?.data?.error || 'Failed to create test account'
      });
    }
  };

  const analyzeTransaction = async (values) => {
    setLoading(true);
    try {
      const response = await axios.post('/api/analyze-transaction', {
        ...values,
        timestamp: new Date().toISOString(),
        transaction_id: `TXN_${Date.now()}`
      });

      const newTransaction = {
        key: transactions.length + 1,
        ...values,
        ...response.data,
        timestamp: new Date().toLocaleString()
      };

      setTransactions([newTransaction, ...transactions]);
      updateStats([newTransaction, ...transactions]);
      
      notification.success({
        message: 'Transaction Analyzed',
        description: `Risk Level: ${response.data.risk_level} (Score: ${response.data.risk_score})`
      });

      form.resetFields();
    } catch (error) {
      notification.error({
        message: 'Analysis Failed',
        description: error.response?.data?.error || 'Failed to analyze transaction'
      });
    }
    setLoading(false);
  };

  const updateStats = (transactionList) => {
    const stats = transactionList.reduce((acc, t) => {
      acc.total++;
      acc[t.risk_level?.toLowerCase()] = (acc[t.risk_level?.toLowerCase()] || 0) + 1;
      return acc;
    }, { total: 0, high: 0, medium: 0, low: 0 });
    setStats(stats);
  };

  const columns = [
    {
      title: 'Transaction ID',
      dataIndex: 'transaction_id',
      key: 'transaction_id',
    },
    {
      title: 'Amount',
      dataIndex: 'amount',
      key: 'amount',
      render: (amount) => `${parseFloat(amount).toLocaleString()}`,
    },
    {
      title: 'From',
      dataIndex: 'sender_account',
      key: 'sender_account',
    },
    {
      title: 'To',
      dataIndex: 'receiver_account',
      key: 'receiver_account',
    },
    {
      title: 'ML Risk',
      dataIndex: 'ml_risk_score',
      key: 'ml_risk_score',
    },
    {
      title: 'Blockchain Risk',
      dataIndex: 'blockchain_risk_score',
      key: 'blockchain_risk_score',
    },
    {
      title: 'Combined Risk',
      dataIndex: 'risk_score',
      key: 'risk_score',
    },
    {
      title: 'Risk Level',
      dataIndex: 'risk_level',
      key: 'risk_level',
      render: (level) => {
        const color = level === 'HIGH' ? 'red' : level === 'MEDIUM' ? 'orange' : 'green';
        return <Tag color={color}>{level}</Tag>;
      },
    },
    {
      title: 'Timestamp',
      dataIndex: 'timestamp',
      key: 'timestamp',
    },
  ];

  const pieData = [
    { name: 'Low Risk', value: stats.low, color: '#52c41a' },
    { name: 'Medium Risk', value: stats.medium, color: '#faad14' },
    { name: 'High Risk', value: stats.high, color: '#ff4d4f' },
  ];

  return (
    <Layout className="app-layout">
      <Header className="app-header">
        <h1>AlgoGuard - Blockchain Money Muling Detection</h1>
      </Header>
      <Content className="app-content">
        {/* Network Status Alert */}
        {networkStatus && (
          <Alert
            message={`Algorand ${networkStatus.network?.toUpperCase()} Network Status`}
            description={
              networkStatus.connected 
                ? `Connected - Last Round: ${networkStatus.last_round}` 
                : `Disconnected - ${networkStatus.error}`
            }
            type={networkStatus.connected ? "success" : "error"}
            showIcon
            style={{ marginBottom: 16 }}
          />
        )}

        <Tabs defaultActiveKey="1">
          <TabPane tab="Transaction Analysis" key="1">
            <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
              <Col span={6}>
                <Card>
                  <Statistic title="Total Transactions" value={stats.total} />
                </Card>
              </Col>
              <Col span={6}>
                <Card>
                  <Statistic title="High Risk" value={stats.high} valueStyle={{ color: '#ff4d4f' }} />
                </Card>
              </Col>
              <Col span={6}>
                <Card>
                  <Statistic title="Medium Risk" value={stats.medium} valueStyle={{ color: '#faad14' }} />
                </Card>
              </Col>
              <Col span={6}>
                <Card>
                  <Statistic title="Low Risk" value={stats.low} valueStyle={{ color: '#52c41a' }} />
                </Card>
              </Col>
            </Row>

            <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
              <Col span={12}>
                <Card title="Analyze New Transaction">
                  <Form form={form} onFinish={analyzeTransaction} layout="vertical">
                    <Form.Item name="amount" label="Amount" rules={[{ required: true }]}>
                      <Input type="number" placeholder="Enter transaction amount" />
                    </Form.Item>
                    <Form.Item name="sender_account" label="Sender Account" rules={[{ required: true }]}>
                      <Input placeholder="Enter sender account ID" />
                    </Form.Item>
                    <Form.Item name="receiver_account" label="Receiver Account" rules={[{ required: true }]}>
                      <Input placeholder="Enter receiver account ID" />
                    </Form.Item>
                    <Button type="primary" htmlType="submit" loading={loading} block>
                      Analyze Transaction
                    </Button>
                  </Form>
                </Card>
              </Col>
              <Col span={12}>
                <Card title="Risk Distribution">
                  <ResponsiveContainer width="100%" height={200}>
                    <PieChart>
                      <Pie
                        data={pieData}
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        dataKey="value"
                      >
                        {pieData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </Card>
              </Col>
            </Row>

            <Card title="Recent Transactions">
              <Table 
                columns={columns} 
                dataSource={transactions} 
                pagination={{ pageSize: 10 }}
                scroll={{ x: true }}
              />
            </Card>
          </TabPane>

          <TabPane tab="Algorand Integration" key="2">
            <Row gutter={[16, 16]}>
              <Col span={12}>
                <Card title="Network Information">
                  {networkStatus && (
                    <Space direction="vertical" style={{ width: '100%' }}>
                      <Statistic title="Network" value={networkStatus.network?.toUpperCase()} />
                      <Statistic title="Last Round" value={networkStatus.last_round} />
                      <Statistic title="Connection Status" value={networkStatus.connected ? "Connected" : "Disconnected"} />
                    </Space>
                  )}
                </Card>
              </Col>
              <Col span={12}>
                <Card title="Test Account" extra={
                  <Button onClick={createTestAccount}>Create Test Account</Button>
                }>
                  {testAccount ? (
                    <Space direction="vertical" style={{ width: '100%' }}>
                      <div><strong>Address:</strong> {testAccount.address}</div>
                      <div><strong>Mnemonic:</strong> {testAccount.mnemonic}</div>
                      <Alert 
                        message="Save this mnemonic securely!" 
                        description="This is a testnet account for demonstration purposes only."
                        type="warning" 
                        showIcon 
                      />
                    </Space>
                  ) : (
                    <div>No test account created yet. Click "Create Test Account" to generate one.</div>
                  )}
                </Card>
              </Col>
            </Row>

            <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
              <Col span={24}>
                <Card title="AlgoGuard Smart Contract Features">
                  <Row gutter={[16, 16]}>
                    <Col span={6}>
                      <Card size="small">
                        <Statistic title="Risk Registry" value="On-Chain" />
                        <p>Store risk assessments on Algorand blockchain</p>
                      </Card>
                    </Col>
                    <Col span={6}>
                      <Card size="small">
                        <Statistic title="Reputation System" value="Decentralized" />
                        <p>Community-driven risk reporting</p>
                      </Card>
                    </Col>
                    <Col span={6}>
                      <Card size="small">
                        <Statistic title="Governance" value="Token-Based" />
                        <p>Vote on risk thresholds and parameters</p>
                      </Card>
                    </Col>
                    <Col span={6}>
                      <Card size="small">
                        <Statistic title="Incentives" value="Reward System" />
                        <p>Earn tokens for accurate reporting</p>
                      </Card>
                    </Col>
                  </Row>
                </Card>
              </Col>
            </Row>
          </TabPane>
        </Tabs>
      </Content>
    </Layout>
  );
}

export default App;