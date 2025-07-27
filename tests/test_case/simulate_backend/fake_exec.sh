#!/bin/bash
# Giả lập việc tải mã độc về /tmp
echo -e '#!/bin/bash\necho "🔥 Mã độc giả lập đang chạy..."' > /tmp/a.sh
chmod +x /tmp/a.sh

echo -e '#!/bin/bash\necho "Chạy: /tmp/shell"' > /tmp/shell
chmod +x /tmp/shell

echo -e '#!/bin/bash\necho "Chạy: /tmp/my_script.sh"' > /tmp/my_script.sh
chmod +x /tmp/my_script.sh

