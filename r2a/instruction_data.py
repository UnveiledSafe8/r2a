INSTRUCTION_SET = {
    "_next_field": "opcode",
    "_nodes": {
        0b10111: {
            "_instruction": {"mnemonic": "auipc", "instr_type": "U", "opcode": 0b10111}
        },

        0b110111: {
            "_instruction": {"mnemonic": "lui", "instr_type": "U", "opcode": 0b110111}
        },

        0b1101111: {
            "_instruction": {"mnemonic": "jal", "instr_type": "J", "opcode": 0b1101111}
        },

        0b1000011: {
            "_instruction": {"mnemonic": "fmadd", "instr_type": "R4", "opcode": 0b1000011}
        },

        0b1000111: {
            "_instruction": {"mnemonic": "fmsub", "instr_type": "R4", "opcode": 0b1000111}
        },

        0b1001011: {
            "_instruction": {"mnemonic": "fnmsub", "instr_type": "R4", "opcode": 0b1001011}
        },

        0b1001111: {
            "_instruction": {"mnemonic": "fnmadd", "instr_type": "R4", "opcode": 0b1001111}
        },

        0b1111: {
            "_next_field": "funct3",
            "_nodes": {
                0b0: {
                    "_instruction": {"mnemonic": "fence", "instr_type": "Misc", "opcode": 0b1111, "funct3": 0b0}
                },

                0b1: {
                    "_instruction": {"mnemonic": "fence.i", "instr_type": "Misc", "opcode": 0b1111, "funct3": 0b1}
                }
            }
        },

        0b100011: {
            "_next_field": "funct3",
            "_nodes": {
                0b0: {
                    "_instruction": {"mnemonic": "sb", "instr_type": "S", "opcode": 0b100011, "funct3": 0b0}
                },

                0b1: {
                    "_instruction": {"mnemonic": "sh", "instr_type": "S", "opcode": 0b100011, "funct3": 0b1}
                },

                0b10: {
                    "_instruction": {"mnemonic": "sw", "instr_type": "S", "opcode": 0b100011, "funct3": 0b10}
                },

                0b11: {
                    "_instruction": {"mnemonic": "sd", "instr_type": "S", "opcode": 0b100011, "funct3": 0b11}
                }
            }
        },

        0b100111: {
            "_next_field": "funct3",
            "_nodes": {
                0b10: {
                    "_instruction": {"mnemonic": "fsw", "instr_type": "S", "opcode": 0b100111, "funct3": 0b10}
                },

                0b11: {
                    "_instruction": {"mnemonic": "fsd", "instr_type": "S", "opcode": 0b100111, "funct3": 0b11}
                },

                0b100: {
                    "_instruction": {"mnemonic": "fsq", "instr_type": "S", "opcode": 0b100111, "funct3": 0b100}
                }
            }
        },

        0b1100011: {
            "_next_field": "funct3",
            "_nodes": {
                0b0: {
                    "_instruction": {"mnemonic": "beq", "instr_type": "B", "opcode": 0b1100011, "funct3": 0b0}
                },

                0b1: {
                    "_instruction": {"mnemonic": "bne", "instr_type": "B", "opcode": 0b1100011, "funct3": 0b1}
                },

                0b100: {
                    "_instruction": {"mnemonic": "blt", "instr_type": "B", "opcode": 0b1100011, "funct3": 0b100}
                },

                0b101: {
                    "_instruction": {"mnemonic": "bge", "instr_type": "B", "opcode": 0b1100011, "funct3": 0b101}
                },

                0b110: {
                    "_instruction": {"mnemonic": "bltu", "instr_type": "B", "opcode": 0b1100011, "funct3": 0b110}
                },

                0b111: {
                    "_instruction": {"mnemonic": "bgeu", "instr_type": "B", "opcode": 0b1100011, "funct3": 0b111}
                }
            }
        },

        0b11: {
            "_next_field": "funct3",
            "_nodes": {
                0b0: {
                    "_instruction": {"mnemonic": "lb", "instr_type": "I", "opcode": 0b11, "funct3": 0b0}
                },

                0b1: {
                    "_instruction": {"mnemonic": "lh", "instr_type": "I", "opcode": 0b11, "funct3": 0b1}
                },

                0b10: {
                    "_instruction": {"mnemonic": "lw", "instr_type": "I", "opcode": 0b11, "funct3": 0b10}
                },

                0b11: {
                    "_instruction": {"mnemonic": "ld", "instr_type": "I", "opcode": 0b11, "funct3": 0b11}
                },

                0b100: {
                    "_instruction": {"mnemonic": "lbu", "instr_type": "I", "opcode": 0b11, "funct3": 0b100}
                },

                0b101: {
                    "_instruction": {"mnemonic": "lhu", "instr_type": "I", "opcode": 0b11, "funct3": 0b101}
                },

                0b110: {
                    "_instruction": {"mnemonic": "lwu", "instr_type": "I", "opcode": 0b11, "funct3": 0b110}
                }
            }
        },

        0b111: {
            "_next_field": "funct3",
            "_nodes": {
                0b10: {
                    "_instruction": {"mnemonic": "flw", "instr_type": "I", "opcode": 0b111, "funct3": 0b10}
                },

                0b11: {
                    "_instruction": {"mnemonic": "fld", "instr_type": "I", "opcode": 0b111, "funct3": 0b11}
                },

                0b100: {
                    "_instruction": {"mnemonic": "flq", "instr_type": "I", "opcode": 0b111, "funct3": 0b100}
                }
            }
        },

        0b10011: {
            "_next_field": "funct3",
            "_nodes": {
                0b0: {
                    "_instruction": {"mnemonic": "addi", "instr_type": "I", "opcode": 0b10011, "funct3": 0b0}
                },

                0b1: {
                    "_next_field": "funct7",
                    "_nodes": {
                        # Treat funct7 as always present in the decoding tree, even when its bits overlap with shamt in 64-bit instructions
                        # Define separate funct7 keys for 32-bit and 64-bit variants accordingly
                        # This lets the decoder traverse the tree uniformly without extra logic for funct6 or special cases
                        # EVen if a 64-bit variant happens to match with the 32-bit variant both instructions are effectively equivalent in such a case
                        0b0: {
                            "_instruction": {"mnemonic": "slli", "instr_type": "I", "opcode": 0b10011, "funct3": 0b1, "funct7": 0b0}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "slli", "instr_type": "I", "opcode": 0b10011, "funct3": 0b1, "funct6": 0b0}
                        }
                    }
                },

                0b10: {
                    "_instruction": {"mnemonic": "slti", "instr_type": "I", "opcode": 0b10011, "funct3": 0b10}
                },

                0b11: {
                    "_instruction": {"mnemonic": "sltiu", "instr_type": "I", "opcode": 0b10011, "funct3": 0b11}
                },

                0b100: {
                    "_instruction": {"mnemonic": "xori", "instr_type": "I", "opcode": 0b10011, "funct3": 0b100}
                },

                0b101: {
                    "_next_field": "funct7",
                    "_nodes": {
                        # Treat funct7 as always present in the decoding tree, even when its bits overlap with shamt in 64-bit instructions
                        # Define separate funct7 keys for 32-bit and 64-bit variants accordingly
                        # This lets the decoder traverse the tree uniformly without extra logic for funct6 or special cases
                        # EVen if a 64-bit variant happens to match with the 32-bit variant both instructions are effectively equivalent in such a case
                        0b0: {
                            "_instruction": {"mnemonic": "srli", "instr_type": "I", "opcode": 0b10011, "funct3": 0b101, "funct7": 0b0}
                        },

                        0b100000: {
                            "_instruction": {"mnemonic": "srai", "instr_type": "I", "opcode": 0b10011, "funct3": 0b101, "funct7": 0b100000}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "srli", "instr_type": "I", "opcode": 0b10011, "funct3": 0b101, "funct6": 0b0}
                        },

                        0b100001: {
                            "_instruction": {"mnemonic": "srai", "instr_type": "I", "opcode": 0b10011, "funct3": 0b101, "funct6": 0b10000}
                        }
                    }
                },

                0b110: {
                    "_instruction": {"mnemonic": "ori", "instr_type": "I", "opcode": 0b10011, "funct3": 0b110}
                },

                0b111: {
                    "_instruction": {"mnemonic": "andi", "instr_type": "I", "opcode": 0b10011, "funct3": 0b111}
                }
            }
        },

        0b11011: {
            "_next_field": "funct3",
            "_nodes": {
                0b0: {
                    "_instruction": {"mnemonic": "addiw", "instr_type": "I", "opcode": 0b11011, "funct3": 0b0}
                },
                0b1: {
                    "_instruction": {"mnemonic": "slliw", "instr_type": "I", "opcode": 0b11011, "funct3": 0b1}
                },
                0b101: {
                    "_next_field": "funct7",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "srliw", "instr_type": "I", "opcode": 0b11011, "funct3": 0b101, "funct7": 0b0}
                        },

                        0b100000: {
                            "_instruction": {"mnemonic": "sraiw", "instr_type": "I", "opcode": 0b11011, "funct3": 0b101, "funct7": 0b100000}
                        }
                    }
                }
            }
        },

        0b1100111: {
            "_next_field": "funct3",
            "_nodes": {
                0b0: {
                    "_instruction": {"mnemonic": "jalr", "instr_type": "I", "opcode": 0b1100111, "funct3": 0b0}
                }
            }
        },

        0b1110011: {
            "_next_field": "funct3",
            "_nodes": {
                0b0: {
                    "_next_field": "imm",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "ecall", "instr_type": "I", "opcode": 0b1110011, "funct3": 0b0, "imm": 0b0, "rs1": 0b0, "rd": 0b0}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "ebreak", "instr_type": "I", "opcode": 0b1110011, "funct3": 0b0, "imm": 0b1, "rs1": 0b0, "rd": 0b0}
                        }
                    }
                },
                0b1: {
                    "_instruction": {"mnemonic": "csrrw", "instr_type": "I", "opcode": 0b1110011, "funct3": 0b1}
                },
                0b10: {
                    "_instruction": {"mnemonic": "csrrs", "instr_type": "I", "opcode": 0b1110011, "funct3": 0b10}
                },
                0b11: {
                    "_instruction": {"mnemonic": "csrrc", "instr_type": "I", "opcode": 0b1110011, "funct3": 0b11}
                },
                0b101: {
                    "_instruction": {"mnemonic": "csrrwi", "instr_type": "I", "opcode": 0b1110011, "funct3": 0b101}
                },
                0b110: {
                    "_instruction": {"mnemonic": "csrrsi", "instr_type": "I", "opcode": 0b1110011, "funct3": 0b110}
                },
                0b111: {
                    "_instruction": {"mnemonic": "csrrci", "instr_type": "I", "opcode": 0b1110011, "funct3": 0b111}
                }
            }
        },

        0b101111: {
            "_next_field": "funct5",
            "_nodes": {
                0b0: {
                    "_instruction": {"mnemonic": "amoadd", "instr_type": "R", "opcode": 0b101111, "funct5": 0b0}
                },
                0b1: {
                    "_instruction": {"mnemonic": "amoswap", "instr_type": "R", "opcode": 0b101111, "funct5": 0b1}
                },
                0b10: {
                    "_instruction": {"mnemonic": "lr", "instr_type": "R", "opcode": 0b101111, "funct5": 0b10}
                },
                0b11: {
                    "_instruction": {"mnemonic": "sc", "instr_type": "R", "opcode": 0b101111, "funct5": 0b11}
                },
                0b1100: {
                    "_instruction": {"mnemonic": "amoand", "instr_type": "R", "opcode": 0b101111, "funct5": 0b1100}
                },
                0b1000: {
                    "_instruction": {"mnemonic": "amoor", "instr_type": "R", "opcode": 0b101111, "funct5": 0b1000}
                },
                0b100: {
                    "_instruction": {"mnemonic": "amoxor", "instr_type": "R", "opcode": 0b101111, "funct5": 0b100}
                },
                0b10100: {
                    "_instruction": {"mnemonic": "amomax", "instr_type": "R", "opcode": 0b101111, "funct5": 0b10100}
                },
                0b10000: {
                    "_instruction": {"mnemonic": "amomin", "instr_type": "R", "opcode": 0b101111, "funct5": 0b10000}
                },
                0b11100: {
                    "_instruction": {"mnemonic": "amomaxu", "instr_type": "R", "opcode": 0b101111, "funct5": 0b11100}
                },
                0b11000: {
                    "_instruction": {"mnemonic": "amominu", "instr_type": "R", "opcode": 0b101111, "funct5": 0b11000}
                },
            }
        },

        0b110011: {
            "_next_field": "funct3",
            "_nodes": {
                0b0: {
                    "_next_field": "funct7",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "add", "instr_type": "R", "opcode": 0b110011, "funct3": 0b0, "funct7": 0b0}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "mul", "instr_type": "R", "opcode": 0b110011, "funct3": 0b0, "funct7": 0b1}
                        },

                        0b100000: {
                            "_instruction": {"mnemonic": "sub", "instr_type": "R", "opcode": 0b110011, "funct3": 0b0, "funct7": 0b100000}
                        }
                    }
                },

                0b1: {
                    "_next_field": "funct7",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "sll", "instr_type": "R", "opcode": 0b110011, "funct3": 0b1, "funct7": 0b0}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "mulh", "instr_type": "R", "opcode": 0b110011, "funct3": 0b1, "funct7": 0b1}
                        }
                    }
                },

                0b10: {
                    "_next_field": "funct7",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "slt", "instr_type": "R", "opcode": 0b110011, "funct3": 0b10, "funct7": 0b0}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "mulhsu", "instr_type": "R", "opcode": 0b110011, "funct3": 0b10, "funct7": 0b1}
                        }
                    }
                },

                0b11: {
                    "_next_field": "funct7",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "sltu", "instr_type": "R", "opcode": 0b110011, "funct3": 0b11, "funct7": 0b0}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "mulu", "instr_type": "R", "opcode": 0b110011, "funct3": 0b11, "funct7": 0b1}
                        }
                    }
                },

                0b100: {
                    "_next_field": "funct7",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "xor", "instr_type": "R", "opcode": 0b110011, "funct3": 0b100, "funct7": 0b0}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "div", "instr_type": "R", "opcode": 0b110011, "funct3": 0b100, "funct7": 0b1}
                        }
                    }
                },

                0b101: {
                    "_next_field": "funct7",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "srl", "instr_type": "R", "opcode": 0b110011, "funct3": 0b101, "funct7": 0b0}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "divu", "instr_type": "R", "opcode": 0b110011, "funct3": 0b101, "funct7": 0b1}
                        },

                        0b100000: {
                            "_instruction": {"mnemonic": "sra", "instr_type": "R", "opcode": 0b110011, "funct3": 0b101, "funct7": 0b100000}
                        }
                    }
                },

                0b110: {
                    "_next_field": "funct7",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "or", "instr_type": "R", "opcode": 0b110011, "funct3": 0b110, "funct7": 0b0}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "rem", "instr_type": "R", "opcode": 0b110011, "funct3": 0b110, "funct7": 0b1}
                        }
                    }
                },

                0b111: {
                    "_next_field": "funct7",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "and", "instr_type": "R", "opcode": 0b110011, "funct3": 0b111, "funct7": 0b0}
                        },
                        
                        0b1: {
                            "_instruction": {"mnemonic": "remu", "instr_type": "R", "opcode": 0b110011, "funct3": 0b111, "funct7": 0b1}
                        }
                    }
                }
            }
        },

        0b111011: {
            "_next_field": "funct3",
            "_nodes": {
                0b0: {
                    "_next_field": "funct7",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "addw", "instr_type": "R", "opcode": 0b111011, "funct3": 0b0, "funct7": 0b0}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "mulw", "instr_type": "R", "opcode": 0b111011, "funct3": 0b0, "funct7": 0b1}
                        },

                        0b100000: {
                            "_instruction": {"mnemonic": "subw", "instr_type": "R", "opcode": 0b111011, "funct3": 0b0, "funct7": 0b100000}
                        }
                    }
                },

                0b1: {
                    "_next_field": "funct7",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "sllw", "instr_type": "R", "opcode": 0b111011, "funct3": 0b1, "funct7": 0b0}
                        }
                    }
                },

                0b100: {
                    "_next_field": "funct7",
                    "_nodes": {
                        0b1: {
                            "_instruction": {"mnemonic": "divw", "instr_type": "R", "opcode": 0b111011, "funct3": 0b100, "funct7": 0b1}
                        }
                    }
                },

                0b101: {
                    "_next_field": "funct7",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "srlw", "instr_type": "R", "opcode": 0b111011, "funct3": 0b101, "funct7": 0b0}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "divuw", "instr_type": "R", "opcode": 0b111011, "funct3": 0b101, "funct7": 0b1}
                        },

                        0b100000: {
                            "_instruction": {"mnemonic": "sraw", "instr_type": "R", "opcode": 0b111011, "funct3": 0b101, "funct7": 0b100000}
                        }
                    }
                },

                0b110: {
                    "_next_field": "funct7",
                    "_nodes": {
                        0b1: {
                            "_instruction": {"mnemonic": "remw", "instr_type": "R", "opcode": 0b111011, "funct3": 0b110, "funct7": 0b1}
                        }
                    }
                },

                0b111: {
                    "_next_field": "funct7",
                    "_nodes": {
                        0b1: {
                            "_instruction": {"mnemonic": "remuw", "instr_type": "R", "opcode": 0b111011, "funct3": 0b111, "funct7": 0b1}
                        }
                    }
                }
            }
        },

        0b1010011: {
            #Narrow by funct5 first since this largely determines if the instruction uses rm or funct3
            "_next_field": "funct5",
            "_nodes": {
                0b0: {
                    "_instruction": {"mnemonic": "fadd", "instr_type": "R", "opcode": 0b1010011, "funct5": 0b0}
                },

                0b1: {
                    "_instruction": {"mnemonic": "fsub", "instr_type": "R", "opcode": 0b1010011, "funct5": 0b1}
                },

                0b10: {
                    "_instruction": {"mnemonic": "fmul", "instr_type": "R", "opcode": 0b1010011, "funct5": 0b10}
                },

                0b11: {
                    "_instruction": {"mnemonic": "fdiv", "instr_type": "R", "opcode": 0b1010011, "funct5": 0b11}
                },

                0b1011: {
                    "_instruction": {"mnemonic": "fsqrt", "instr_type": "R", "opcode": 0b1010011, "funct5": 0b1011, "rs2": 0b0}
                },

                0b100: {
                    "_next_field": "funct3",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "fsgnj", "instr_type": "R", "opcode": 0b1010011, "funct3": 0b0, "funct5": 0b100}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "fsgnjn", "instr_type": "R", "opcode": 0b1010011, "funct3": 0b1, "funct5": 0b100}
                        },

                        0b10: {
                            "_instruction": {"mnemonic": "fsgnjx", "instr_type": "R", "opcode": 0b1010011, "funct3": 0b10, "funct5": 0b100}
                        }
                    }
                },

                0b101: {
                    "_next_field": "funct3",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "fmin", "instr_type": "R", "opcode": 0b1010011, "funct3": 0b0, "funct5": 0b101}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "fmax", "instr_type": "R", "opcode": 0b1010011, "funct3": 0b1, "funct5": 0b101}
                        }
                    }
                },

                0b1000: {
                    "_instruction": {"mnemonic": "fcvt", "instr_type": "R", "opcode": 0b1010011, "funct5": 0b1000}
                },

                0b10100: {
                    "_next_field": "funct3",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "fle", "instr_type": "R", "opcode": 0b1010011, "funct3": 0b0, "funct5": 0b10100}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "flt", "instr_type": "R", "opcode": 0b1010011, "funct3": 0b1, "funct5": 0b10100}
                        },

                        0b10: {
                            "_instruction": {"mnemonic": "feq", "instr_type": "R", "opcode": 0b1010011, "funct3": 0b10, "funct5": 0b10100}
                        }
                    }
                },

                0b11000: {
                    "_instruction": {"mnemonic": "fcvt", "instr_type": "R", "opcode": 0b1010011, "funct5": 0b11000}
                },

                0b11010: {
                    "_instruction": {"mnemonic": "fcvt", "instr_type": "R", "opcode": 0b1010011, "funct5": 0b11010}
                },

                0b11100: {
                    "_next_field": "funct3",
                    "_nodes": {
                        0b0: {
                            "_instruction": {"mnemonic": "fmv", "instr_type": "R", "opcode": 0b1010011, "funct3": 0b0, "funct5": 0b11100}
                        },

                        0b1: {
                            "_instruction": {"mnemonic": "fclass", "instr_type": "R", "opcode": 0b1010011, "funct3": 0b1, "funct5": 0b11100}
                        }
                    }
                },

                0b11110: {
                    "_instruction": {"mnemonic": "fmv", "instr_type": "R", "opcode": 0b1010011, "funct5": 0b11110}
                }       
            }
        }
    }
}