CREATE TABLE IF NOT EXISTS `category` (
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `type` VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    classified_count SMALLINT NOT NULL,
    url VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT NOW(),
    updated_at DATETIME NOT NULL DEFAULT NOW(),
    UNIQUE (`type`, slug)
);

CREATE TABLE IF NOT EXISTS `classified` (
    external_id INT NOT NULL,
    category_id INT UNSIGNED NOT NULL,
    slug VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    has_picture TINYINT(1) NOT NULL,
    is_commercial TINYINT(1) NOT NULL,
    publish_date DATETIME NOT NULL,
    created_at DATETIME NOT NULL DEFAULT NOW(),
    updated_at DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY (external_id),
    CONSTRAINT fk_classified_category FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE
);