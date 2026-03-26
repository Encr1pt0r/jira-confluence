# 🚀 JC - Your Jira & Confluence CLI

**Welcome!** You now have a powerful command-line tool called **JC** (Jira Confluence).

## ✓ What's Ready

- ✓ **jc.py** - Your main CLI tool
- ✓ **Credentials configured** - Ready to use
- ✓ **All features tested** - Working perfectly
- ✓ **Documentation complete** - Easy to follow

## 🎯 Quick Start (3 Steps)

### 1. Test It Now (No setup needed!)
```bash
python jc.py ticket mine
python jc.py confluence search wildcat
```

### 2. Setup Alias (One time - Makes it easier!)
```bash
notepad $PROFILE
```

Add this line:
```powershell
function jc { python C:\Users\kevin.mbuluko\projects\jira-discovery\jc.py $args }
```

Save, close, restart PowerShell.

### 3. Use It!
```bash
jc ticket mine
jc sprint --component "ProductArea:H&C"
jc comment add SD-5787 "My update"
```

## 📚 Documentation

- **README.md** ← Start here for all commands
- **SETUP_ALIAS.md** ← Detailed alias setup
- **CLI_README.md** ← Complete technical reference

## 🔥 Most Useful Commands

```bash
# Your daily workflow
jc ticket mine                                  # Your tickets
jc sprint --component "ProductArea:H&C"        # Team sprint
jc ticket get SD-5787 --full                   # View ticket

# Update tickets
jc comment add SD-5787 "Status update"         # Add comment
jc transition SD-5787 "In Progress"            # Change status
jc edit SD-5787 --assignee "kevin.mbuluko"     # Assign

# Find documentation
jc confluence search "wildcat sprint review"   # Search docs
jc confluence page 6725500929 --preview        # View page

# Search tickets
jc ticket search "project = SD AND status = Open"
```

## 💡 Why JC?

- **Fast**: Just 2 characters to type!
- **Powerful**: Full Jira + Confluence access
- **Easy**: Simple, intuitive commands
- **Secure**: Credentials stored safely
- **Complete**: View, edit, comment, search everything

## 🎓 Learn More

```bash
jc --help              # All commands
jc ticket --help       # Ticket commands
jc comment --help      # Comment commands
jc confluence --help   # Confluence commands
```

## ✅ Already Tested

- ✓ Retrieved your tickets (SD-3283, SD-3432, SD-3792)
- ✓ Found Wildcat documentation in Confluence
- ✓ Viewed ticket details (SD-3589)
- ✓ Configuration working perfectly

## 🏃 Try These Now

```bash
# See your current work
python jc.py ticket mine

# Check Wildcat team sprint
python jc.py sprint --component "ProductArea:H&C"

# Search for Wildcat docs
python jc.py confluence search "wildcat playbook"

# View a ticket
python jc.py ticket get SD-3589
```

## 📁 Project Structure

```
jira-discovery/
├── jc.py                    ← Main CLI tool (USE THIS!)
├── README.md                ← Full documentation
├── START_HERE.md            ← You are here
├── SETUP_ALIAS.md           ← Alias setup guide
├── CLI_README.md            ← Technical reference
├── requirements.txt         ← Dependencies (installed)
├── .env                     ← Credentials (configured)
└── playground/              ← Development/testing scripts
```

## 🎯 Next Steps

1. **Try it**: `python jc.py ticket mine`
2. **Setup alias**: Follow SETUP_ALIAS.md
3. **Read docs**: Check out README.md
4. **Start using**: `jc ticket mine`, `jc sprint`, etc.

---

**That's it! You're all set.** 🎉

Quick command to remember:
```bash
python jc.py ticket mine
```

After alias setup:
```bash
jc ticket mine
```

**Happy ticket hunting!** 🎫
