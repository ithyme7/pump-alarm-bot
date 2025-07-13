-- query.sql
-- Dit is een kopie van de werkende query (V6) op Dune, voor referentie.

SELECT
    t.token_bought_address,
    UPPER(erc.symbol) AS token_symbol, -- Probeer het symbool te vinden
    SUM(t.amount_usd) AS total_volume_usd
FROM
    dex.trades AS t
LEFT JOIN tokens.erc20 AS erc ON t.blockchain = erc.blockchain AND t.token_bought_address = erc.contract_address
WHERE
    t.project = 'uniswap'
    AND t.version = '3'
    AND t.blockchain = 'ethereum'
    AND t.block_time > NOW() - INTERVAL '24' HOUR
    AND t.amount_usd > 1000
GROUP BY
    t.token_bought_address,
    erc.symbol
ORDER BY
    total_volume_usd DESC
LIMIT 10