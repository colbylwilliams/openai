//
//  Model.swift
//  OpenAI
//
//  Created by Colby L Williams on 1/24/23.
//

import UIKit
import Foundation
import SwiftyChat

struct Message: ChatMessage {
    let id = UUID()
    var user: User
    var messageKind: ChatMessageKind
    var isSender: Bool { user != User.AI }
    var date: Date = Date()
}

struct User: ChatUser {
//    static let AI = User(userName: "AI", avatar: UIImage(named: "OpenAIAvatar"))
//    static let Me = User(userName: "You", avatar: UIImage(named: "ColbyAvatar"))
    static let AI = User(userName: "AI")
    static let Me = User(userName: "You")

    var id: String { userName }
    var userName: String
    var avatar: UIImage?
    var avatarURL: URL?
}
