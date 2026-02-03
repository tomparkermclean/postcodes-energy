# Contributing to postcodes.energy

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Ways to Contribute

### 🐛 Report Bugs

Found a bug? Please [open an issue](https://github.com/yourusername/postcodes-energy/issues) with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Browser/device information
- Screenshots if applicable

### 💡 Suggest Features

Have an idea? [Open an issue](https://github.com/yourusername/postcodes-energy/issues) with:

- Clear description of the feature
- Use case / why it's useful
- Proposed implementation (if you have ideas)

### 📝 Improve Documentation

- Fix typos or unclear instructions
- Add examples
- Improve setup guides
- Translate documentation

### 🔧 Submit Code

1. **Fork the repository**
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit**: `git commit -m "Add your feature"`
6. **Push**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**

## Code Guidelines

### Frontend (HTML/CSS/JS)

- Use vanilla JavaScript (no frameworks)
- Keep code readable and well-commented
- Follow existing code style
- Ensure mobile responsiveness
- Test in multiple browsers

### Python (Data Processing)

- Follow PEP 8 style guide
- Add docstrings to functions
- Handle errors gracefully
- Test with sample data before full run

## Data Contributions

### Adding Missing DNO Data

If you have access to DNO data not currently included:

1. Check it's openly licensed
2. Add to `DNO_INVENTORY.md`
3. Update `process_data.py` to include it
4. Document the source in `DATA_SOURCES.md`

### Improving Data Processing

- Optimize spatial joins for performance
- Improve boundary simplification
- Better handling of edge cases
- Enhanced error reporting

## Testing

Before submitting:

- [ ] Test data processing with sample data
- [ ] Test frontend with multiple postcodes
- [ ] Check mobile responsiveness
- [ ] Verify map functionality
- [ ] Test export features
- [ ] Check browser console for errors

## Pull Request Process

1. **Update documentation** if you changed functionality
2. **Add your changes** to relevant documentation
3. **Ensure all tests pass** (if applicable)
4. **Request review** from maintainers
5. **Address feedback** promptly

## Commit Message Guidelines

Use clear, descriptive commit messages:

```
Good:
- "Add autocomplete to postcode search"
- "Fix map not centering on boundary"
- "Update SSEN data source documentation"

Bad:
- "Update file"
- "Fix bug"
- "Changes"
```

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Other unprofessional conduct

## Questions?

- Open an issue with the "question" label
- Email: [your-email@postcodes.energy]
- Check existing issues and documentation first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be acknowledged in:
- GitHub contributors page
- Release notes
- README (for significant contributions)

---

Thank you for helping make postcodes.energy better! ⚡
