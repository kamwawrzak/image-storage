from yoyo import step

step(
    apply="""
        CREATE TABLE images (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),
            img_name VARCHAR(255),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            deleted_at DATETIME NULL);
        """,
    rollback="""
        DROP TABLE images
        """
)
