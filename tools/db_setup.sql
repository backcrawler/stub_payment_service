CREATE SEQUENCE IF NOT EXISTS customer_id_seq;

CREATE TABLE IF NOT EXISTS customer (
    id integer NOT NULL DEFAULT nextval('customer_id_seq'),
    userId varchar(128) NOT NULL,
    balance integer NOT NULL
);

ALTER SEQUENCE customer_id_seq OWNED BY customer.id;

CREATE UNIQUE INDEX IF NOT EXISTS user_id_idx ON customer (userId);


CREATE SEQUENCE IF NOT EXISTS paymentKey_id_seq;

CREATE TABLE IF NOT EXISTS paymentKey (
    id integer NOT NULL DEFAULT nextval('paymentKey_id_seq'),
    userId varchar(128) NOT NULL,
    externalKey varchar(128) NOT NULL
);

ALTER SEQUENCE paymentKey_id_seq OWNED BY paymentKey.id;

CREATE UNIQUE INDEX IF NOT EXISTS paymentKey_idx ON paymentKey (userId, externalKey);