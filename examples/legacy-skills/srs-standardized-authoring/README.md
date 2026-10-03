# Nguồn chuẩn skill SRS

`SKILL.md` trong thư mục này là nguồn chuẩn duy nhất cho skill
`srs-standardized-authoring`. Biểu mẫu SRS cùng thuộc repo này tại
`../templates/TEMPLATE-SRS-7-muc.md`.

Không sửa trực tiếp bản runtime ở `tracepro-docs/.claude/skills/`.
Sau khi thay đổi nguồn chuẩn, chạy:

```bash
bash scripts/sync-srs-contract.sh --export ../tracepro-docs
bash scripts/sync-srs-contract.sh --check ../tracepro-docs
```

Khi cần tiếp nhận một thay đổi đã được duyệt ở runtime, nhập nó có chủ đích rồi
kiểm tra diff trước khi commit:

```bash
bash scripts/sync-srs-contract.sh --import ../tracepro-docs
git diff -- Specs/00-CHUAN-TAI-LIEU/skills/srs-standardized-authoring/SKILL.md
```

Quy trình PR: sửa template và `SKILL.md` nguồn chuẩn trong cùng một PR ở repo
`docs`; sau đó chạy export và tạo PR mirror ở `tracepro-docs`. Cả hai PR phải
dùng cùng nội dung `SKILL.md`; lệnh `--check` là điều kiện chốt PR mirror.
